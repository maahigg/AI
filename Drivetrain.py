package org.firstinspires.ftc.teamcode;

import com.qualcomm.hardware.rev.RevHubOrientationOnRobot; 
import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode; 
import com.qualcomm.robotcore.eventloop.opmode.TeleOp; 
import com.qualcomm.robotcore.hardware.DcMotor; 
import com.qualcomm.robotcore.hardware.IMU; 
import com.qualcomm.robotcore.util.ElapsedTime; 
import org.firstinspires.ftc.robotcore.external.navigation.AngleUnit; 
import org.firstinspires.ftc.robotcore.external.navigation.AngularVelocity; 
import org.firstinspires.ftc.robotcore.external.navigation.YawPitchRollAngles; 

// ===================== CLASS / OP MODE DECLARATION =====================
@TeleOp(name = "FGC Tank Drive", group = "TeleOp")
public class TankDrivetrain extends LinearOpMode {


    // HARDWARE OBJECTS

    private DcMotor leftMotor;      // left side drive wheels
    private DcMotor rightMotor;     // right side drive wheels
    private DcMotor leftTransfer;   // left transfer
    private DcMotor rightTransfer;  // right transfer
    private DcMotor intakeMotor;    // motor that spins the intake rollers to pick up game pieces
    private IMU imu;                // the hub's built-in gyro, used for heading hold + anti-tip

    // =================================================================
    // TUNABLE CONSTANTS
    // "static final" means these never change while the program runs and
    // are shared by the whole class. Keeping them all up here means you can
    // tune the robot's feel without hunting through the logic below.
    // =================================================================

    // Joystick deadzone: any stick value with an absolute value smaller than
    // this gets treated as exactly 0. This exists because joysticks rarely
    // rest at PERFECTLY 0.00 — they might drift to 0.01 or -0.02 — which
    // would otherwise cause the robot to creep even when you're not touching
    // the sticks.
    private static final double DEADZONE = 0.05;

    // FEATURE 1: Slew-rate acceleration ramp 
    // SLEW_RATE is the maximum amount motor power is allowed to change per
    // SECOND. A value of 2.5 means power can go from 0.0 to 1.0 (full power)
    // in about 1 / 2.5 = 0.4 seconds. Lower this number to make acceleration
    // gentler (less current spike, less wheel slip); raise it to make the
    // robot feel snappier.
    private static final double SLEW_RATE = 2.5;

    // FEATURE 2: Intake slow mode 
    // Two preset intake speeds. INTAKE_FULL_POWER is used normally.
    // INTAKE_SLOW_POWER is used when "slow mode" is toggled on — slower
    // rollers give game pieces more time to feed in correctly instead of
    // bouncing off or jamming.
    private static final double INTAKE_FULL_POWER = 1.0;
    private static final double INTAKE_SLOW_POWER = 0.35;

    // ---------- FEATURE 3: Speed-based turn scaling ----------
    // This robot is TANK drive, meaning each stick directly controls one
    // side of the robot — there's no separate "turn" stick like arcade
    // drive. Because of that, "turning" really means "how different the
    // left and right power are from each other." If you slam the sticks in
    // opposite directions while already flying forward, the wheels fight
    // the robot's momentum and it can skid or even tip.
    //
    // MIN_TURN_SCALE controls how much that left/right difference gets
    // squashed down at max forward speed. At 0 forward speed, turning is
    // NOT scaled at all (scale = 1.0, full turning authority — good for
    // precise aiming while stopped). At full forward speed, the difference
    // is multiplied by MIN_TURN_SCALE instead (here, 0.35 = 35% of normal),
    // which makes turns much gentler/wider at speed, similar to how a car's
    // steering feels heavier and less twitchy on the highway.
    private static final double MIN_TURN_SCALE = 0.35;

    // ---------- FEATURE 4: Quick turn button ----------
    // While the quick-turn button (left bumper) is held, we ignore normal
    // drive logic entirely and just spin the two sides in opposite
    // directions at this fixed power, letting the robot pivot in place fast
    // — handy for quickly re-aiming when stopped or moving slowly.
    private static final double QUICK_TURN_POWER = 0.6;

    // ---------- FEATURE 5: Heading hold ----------
    // When you're driving "straight" (both sticks roughly equal), tiny
    // mechanical differences between the left and right sides (friction,
    // battery sag, wheel wear) can make the robot slowly curve instead of
    // going dead straight. Heading hold fixes this by reading the gyro's
    // heading and nudging power side-to-side to cancel out any drift.
    //
    // HEADING_KP ("Kp" = proportional gain, a term from PID control) is how
    // aggressively we correct per degree of heading error. Too high and the
    // robot will oscillate/wobble trying to correct; too low and it won't
    // correct fast enough to matter.
    private static final double HEADING_KP = 0.02;

    // We cap how much correction power heading hold is allowed to add, so a
    // big heading error (e.g. right after a turn) can't suddenly slam the
    // robot sideways.
    private static final double MAX_HEADING_CORRECTION = 0.3;

    // Heading hold doesn't lock in the instant you stop turning — it waits
    // this many seconds first. This avoids "fighting" the driver during the
    // brief moment right after finishing a turn, before they've settled
    // into driving straight.
    private static final double HEADING_LOCK_DELAY_SEC = 0.3;

    // ---------- FEATURE 6: Anti-tip / anti-skid protection ----------
    // MAX_SAFE_TILT_DEG: if the robot's pitch (front/back tilt) or roll
    // (side/side tilt) exceeds this many degrees, something is wrong — the
    // robot might be climbing an obstacle too aggressively or about to tip
    // over — so we cut power.
    private static final double MAX_SAFE_TILT_DEG = 12.0;

    // MAX_SAFE_YAW_RATE: if the robot is spinning around its vertical axis
    // faster than this many degrees per second, the wheels are likely
    // skidding/slipping rather than driving under control, so we cut power
    // there too.
    private static final double MAX_SAFE_YAW_RATE = 250.0;

    // TILT_POWER_CUT: when an unsafe condition above is detected, we don't
    // necessarily want to slam to a dead stop (that can make tipping WORSE
    // by throwing the robot's weight forward). Instead we multiply the
    // requested power by this factor (0.4 = drop to 40% power) to calm
    // things down gradually.
    private static final double TILT_POWER_CUT = 0.4;

    // =================================================================
    // STATE VARIABLES
    // =================================================================

    // The actual power currently being sent to each drive motor, AFTER the
    // slew-rate limiter has smoothed it. We need to remember this between
    // loops because the slew limiter's job is to nudge this value toward
    // the target power a little bit at a time, not jump straight to it.
    private double leftPowerActual = 0;
    private double rightPowerActual = 0;

    // Whether intake slow mode is currently turned on. Starts false (full
    // power) until the driver toggles it with the right bumper.
    private boolean intakeSlowMode = false;

    // Remembers whether the right bumper was pressed on the PREVIOUS loop
    // iteration. We need this to detect a "new press" (the exact frame the
    // button goes from not-pressed to pressed) instead of toggling rapidly
    // every single loop while the button is held down (which would just
    // flicker between on/off many times per second).
    private boolean rightBumperLast = false;

    // The heading (in degrees) that heading-hold is currently trying to
    // maintain. It's a "Double" (capital D, the object wrapper) instead of
    // a plain "double" specifically so it can be null, which we use to mean
    // "not currently locked onto any heading."
    private Double headingHoldTarget = null;

    // Stopwatch that tracks how long we've been driving "straight" (no turn
    // input). Used to implement the HEADING_LOCK_DELAY_SEC delay.
    private final ElapsedTime straightTimer = new ElapsedTime();

    // Stopwatch used purely to measure how much real time (dt = "delta
    // time") has passed since the last loop iteration. The slew-rate
    // limiter needs this because "max change per second" only makes sense
    // if you know how many seconds actually passed.
    private final ElapsedTime loopTimer = new ElapsedTime();

    // =================================================================
    // MAIN OP MODE METHOD
    // The FTC SDK automatically calls this once when the driver hits INIT
    // and then again... actually just once total — everything from
    // waitForStart() onward happens after they hit PLAY, and the
    // while-loop below keeps running until they hit STOP.
    // =================================================================
    @Override
    public void runOpMode() {

        // ---------- HARDWARE MAPPING ----------
        // hardwareMap.get(...) looks up a device by the name you gave it in
        // the Driver Station's robot configuration file, and connects our
        // Java variable to that physical device. The string ("leftMotor",
        // etc.) MUST exactly match the name used in your configuration —
        // if it doesn't, the robot will crash on init with a "device not
        // found" error.
        leftMotor = hardwareMap.get(DcMotor.class, "leftMotor");
        rightMotor = hardwareMap.get(DcMotor.class, "rightMotor");
        leftTransfer = hardwareMap.get(DcMotor.class, "leftTransfer");
        rightTransfer = hardwareMap.get(DcMotor.class, "rightTransfer");
        intakeMotor = hardwareMap.get(DcMotor.class, "intakeMotor");

        // ---------- MOTOR DIRECTIONS ----------
        // Motors on opposite sides of a robot are usually mounted mirrored,
        // so "positive power" would spin them opposite ways relative to the
        // robot unless we flip one side. REVERSE/FORWARD here is just
        // correcting for that mechanical mirroring so that positive power
        // always means "drive forward" for BOTH sides.
        leftMotor.setDirection(DcMotor.Direction.REVERSE);
        rightMotor.setDirection(DcMotor.Direction.FORWARD);
        leftTransfer.setDirection(DcMotor.Direction.REVERSE);
        rightTransfer.setDirection(DcMotor.Direction.FORWARD);
        intakeMotor.setDirection(DcMotor.Direction.REVERSE);

        // ---------- ZERO POWER BEHAVIOR ----------
        // BRAKE means that when power is set to 0, the motor controller
        // actively resists motion (like an electronic brake) instead of
        // letting the motor spin freely (FLOAT). BRAKE is generally safer
        // for drivetrains and transfer/intake mechanisms since it stops the
        // robot/mechanism more precisely and prevents unwanted coasting.
        leftMotor.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rightMotor.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        leftTransfer.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rightTransfer.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        intakeMotor.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);

        // ---------- IMU (GYRO) SETUP ----------
        // "imu" here must match the name of the IMU in your hardware
        // configuration (it's built into the Control Hub, but still needs
        // to appear in your config — it usually does by default).
        imu = hardwareMap.get(IMU.class, "imu");

        // The IMU needs to know which way it's physically oriented on the
        // robot so it can translate its raw internal readings into
        // correct robot-relative yaw/pitch/roll. LogoFacingDirection.UP
        // means the RevRobotics logo on the hub points toward the sky, and
        // UsbFacingDirection.FORWARD means the hub's USB ports point toward
        // the front of the robot. If your hub is mounted differently (e.g.
        // lying flat with the logo facing forward, or rotated), CHANGE
        // THESE TWO VALUES to match, or all the gyro math below will be
        // wrong.
        imu.initialize(new IMU.Parameters(
                new RevHubOrientationOnRobot(
                        RevHubOrientationOnRobot.LogoFacingDirection.UP,
                        RevHubOrientationOnRobot.UsbFacingDirection.FORWARD)));

        // Sets the robot's CURRENT heading as "0 degrees." Do this once at
        // start so heading hold and telemetry are relative to however the
        // robot happens to be facing when the op mode starts, not some
        // arbitrary factory-zero direction.
        imu.resetYaw();

        // ---------- INIT TELEMETRY ----------
        // telemetry.addLine/addData queue up text to show on the Driver
        // Station screen; telemetry.update() actually sends/displays it.
        // This just confirms to the driver that init finished successfully
        // and reminds them what the extra buttons do.
        telemetry.addLine("Robot Ready!");
        telemetry.addLine("Right bumper = intake slow mode toggle");
        telemetry.addLine("Left bumper (hold) = quick turn");
        telemetry.update();

        // Pauses here until the driver presses PLAY on the Driver Station.
        // Nothing below this line runs until then.
        waitForStart();

        // Reset both stopwatches right as we start driving so their very
        // first readings are accurate (otherwise they'd include all the
        // time spent sitting in INIT waiting for PLAY).
        loopTimer.reset();
        straightTimer.reset();

        // =============================================================
        // MAIN LOOP
        // opModeIsActive() stays true until the driver hits STOP (or the
        // match timer ends). Everything in here runs over and over, many
        // times per second, for the whole match — this is where all the
        // driving logic lives.
        // =============================================================
        while (opModeIsActive()) {

            // ---- Measure how much time passed since the last loop ----
            // dt = "delta time," the number of SECONDS since we last reset
            // loopTimer. FTC loops usually run every ~10-20 milliseconds,
            // so dt will typically be a small number like 0.015. We need
            // this for the slew-rate math later (max change PER SECOND
            // times the fraction of a second that actually passed).
            double dt = loopTimer.seconds();
            loopTimer.reset();

            // ---- Read the gyro/IMU ----
            // getRobotYawPitchRollAngles() gives us the robot's current
            // orientation: yaw (compass heading, rotation around the
            // vertical axis), pitch (tilting front/back), and roll
            // (tilting side/side).
            YawPitchRollAngles orientation = imu.getRobotYawPitchRollAngles();

            // getRobotAngularVelocity() gives us how FAST the robot is
            // currently rotating around each axis, in degrees per second —
            // different from orientation, which tells us the angle itself.
            AngularVelocity angularVelocity = imu.getRobotAngularVelocity(AngleUnit.DEGREES);

            double heading = orientation.getYaw(AngleUnit.DEGREES);   // compass-style heading, used by heading hold
            double pitch = orientation.getPitch(AngleUnit.DEGREES);   // front/back tilt, used by anti-tip
            double roll = orientation.getRoll(AngleUnit.DEGREES);     // side/side tilt, used by anti-tip
            double yawRate = angularVelocity.zRotationRate;           // spin speed around vertical axis, used by anti-skid

            // ---- Read raw joystick input ----
            // gamepad1.left_stick_y and right_stick_y range from -1 (stick
            // pushed all the way up) to +1 (pulled all the way down) on the
            // FTC SDK's convention. We negate them so pushing the stick UP
            // (away from you) means "drive forward" (positive), which
            // matches how humans intuitively expect a joystick to work.
            double leftStick = -gamepad1.left_stick_y;
            double rightStick = -gamepad1.right_stick_y;

            // Apply the deadzone: snap tiny stick values to exactly zero so
            // the robot doesn't creep from joystick noise when you're not
            // touching the sticks.
            if (Math.abs(leftStick) < DEADZONE) leftStick = 0;
            if (Math.abs(rightStick) < DEADZONE) rightStick = 0;

            // These will hold the power we WANT to send to each motor this
            // loop, before the slew-rate limiter smooths them. They get
            // filled in by one of the two branches below (quick turn vs.
            // normal driving).
            double leftTarget;
            double rightTarget;

            // Is the driver currently holding the quick-turn button?
            boolean quickTurn = gamepad1.left_bumper;

            // =========================================================
            // FEATURE 4: QUICK TURN (branch A)
            // =========================================================
            if (quickTurn) {
                // Figure out which direction to spin. If the driver is also
                // pushing the sticks in some direction, use THAT to decide
                // which way to pivot (so quick turn feels intuitive and
                // responsive to stick direction, not just a fixed spin).
                double turnDir = (leftStick - rightStick) >= 0 ? 1 : -1;

                // But if both sticks are basically centered (driver is just
                // holding the bumper with no stick input at all), default
                // to spinning one fixed direction rather than doing
                // nothing.
                if (Math.abs(leftStick) < DEADZONE && Math.abs(rightStick) < DEADZONE) {
                    turnDir = 1; // default pivot direction when no stick input
                }

                // Spin the two sides in OPPOSITE directions at a fixed
                // power — this is what makes the robot pivot in place
                // around its own center instead of driving forward while
                // turning.
                leftTarget = QUICK_TURN_POWER * turnDir;
                rightTarget = -QUICK_TURN_POWER * turnDir;

                // Quick turn intentionally skips turn scaling (feature 3)
                // and heading hold (feature 5) entirely — those are for
                // normal driving, not deliberate fast pivots. We also
                // release any active heading lock since we're now
                // intentionally changing heading.
                headingHoldTarget = null;
                straightTimer.reset();

            } else {
                // =====================================================
                // NORMAL TANK DRIVE (branch B) — includes features 3 and 5
                // =====================================================

                // Convert the two independent stick values into a
                // "forward" component (how much both sides agree, i.e.
                // overall speed) and a "turn" component (how much they
                // disagree, i.e. how hard we're turning). This is a
                // standard trick: average = forward, half-difference =
                // turn. It lets us apply turn-specific logic (scaling,
                // heading correction) without touching the forward speed.
                double forward = (leftStick + rightStick) / 2.0;
                double turn = (leftStick - rightStick) / 2.0;

                // ---- FEATURE 3: Speed-based turn scaling ----
                // avgSpeed is how fast we're going overall, from 0 (stopped)
                // to 1 (full speed), regardless of direction (hence
                // Math.abs).
                double avgSpeed = Math.abs(forward);

                // turnScale interpolates between 1.0 (full turning
                // authority) at avgSpeed=0 and MIN_TURN_SCALE (reduced
                // turning authority) at avgSpeed=1. E.g. with
                // MIN_TURN_SCALE=0.35: at half speed (avgSpeed=0.5),
                // turnScale = 1 - 0.65*0.5 = 0.675, so turning is already
                // noticeably softened.
                double turnScale = 1.0 - (1.0 - MIN_TURN_SCALE) * avgSpeed;

                // Actually apply that scale to how much turning we allow.
                turn *= turnScale;

                // ---- FEATURE 5: Heading hold ----
                // We only consider engaging heading hold if the driver's
                // RAW stick difference (before scaling) is inside the
                // deadzone — meaning they're not intentionally trying to
                // turn at all right now.
                if (Math.abs(leftStick - rightStick) < DEADZONE) {

                    // Only lock in once we've been going straight for at
                    // least HEADING_LOCK_DELAY_SEC seconds, so we don't
                    // fight the driver the instant they let go of a turn.
                    if (straightTimer.seconds() > HEADING_LOCK_DELAY_SEC) {

                        // The FIRST time we notice we've been straight long
                        // enough, remember the CURRENT heading as our
                        // target to hold. We only set this once per
                        // "straight streak" (it stays non-null until the
                        // driver turns again), which is why we check for
                        // null before overwriting it.
                        if (headingHoldTarget == null) headingHoldTarget = heading;

                        // error = how far off we've drifted from the
                        // target heading, in degrees. Positive means we've
                        // drifted one way, negative the other.
                        double error = headingHoldTarget - heading;

                        // Compass headings wrap around at +/-180 degrees
                        // (i.e. 179 degrees and -179 degrees are actually
                        // only 2 degrees apart, not 358). This loop
                        // "unwraps" the error into the -180..180 range so
                        // the correction math below always takes the
                        // SHORTEST path back to the target heading.
                        while (error > 180) error -= 360;
                        while (error < -180) error += 360;

                        // Proportional correction: bigger error = bigger
                        // correction, scaled by HEADING_KP. Clamped to
                        // +/-MAX_HEADING_CORRECTION so a large error can't
                        // suddenly apply a huge, jarring correction.
                        double correction = Math.max(-MAX_HEADING_CORRECTION,
                                Math.min(MAX_HEADING_CORRECTION, HEADING_KP * error));

                        // Add the correction into our turn value. This will
                        // slightly increase one side's power and decrease
                        // the other's, nudging the robot back toward the
                        // locked heading.
                        turn += correction;
                    }
                    // NOTE: if we're within the deadzone but haven't yet
                    // passed HEADING_LOCK_DELAY_SEC, we intentionally do
                    // nothing here — no correction is applied yet, we're
                    // just waiting.
                } else {
                    // The driver IS actively turning, so heading hold
                    // should NOT be active. Reset the "how long have we
                    // been straight" timer, and clear the locked target so
                    // that next time we go straight, we lock onto the NEW
                    // heading rather than the old one.
                    straightTimer.reset();
                    headingHoldTarget = null;
                }

                // Convert forward + turn back into individual left/right
                // motor power. This is the reverse of the split we did
                // above: left side gets forward+turn, right side gets
                // forward-turn.
                leftTarget = forward + turn;
                rightTarget = forward - turn;
            }

            // =========================================================
            // FEATURE 6: Anti-tip / anti-skid protection
            // This runs AFTER both branches above, so it applies no matter
            // whether we were quick-turning or driving normally — safety
            // should override everything else.
            // =========================================================

            // "unsafe" becomes true if ANY of these conditions are met:
            // tilting too far forward/back, tilting too far side to side,
            // or spinning faster than what a controlled turn should ever
            // produce (which usually means wheels are skidding, not
            // gripping).
            boolean unsafe = Math.abs(pitch) > MAX_SAFE_TILT_DEG
                    || Math.abs(roll) > MAX_SAFE_TILT_DEG
                    || Math.abs(yawRate) > MAX_SAFE_YAW_RATE;

            if (unsafe) {
                // Scale BOTH sides down by the same factor (rather than
                // stopping instantly) so the robot settles down smoothly
                // instead of lurching, which could actually make tipping
                // worse.
                leftTarget *= TILT_POWER_CUT;
                rightTarget *= TILT_POWER_CUT;

                // Drop any heading lock — after an unsafe event the
                // robot's heading has likely changed unpredictably, so the
                // old locked target is no longer meaningful.
                headingHoldTarget = null;
            }

            // ---- Safety clamp ----
            // No matter what math happened above, motor power must never
            // be sent outside the valid range of -1.0 to 1.0. This is a
            // final safety net in case any combination of turn scaling +
            // heading correction + quick turn accidentally added up to
            // something out of range.
            leftTarget = clamp(leftTarget, -1, 1);
            rightTarget = clamp(rightTarget, -1, 1);

            // =========================================================
            // FEATURE 1: Slew-rate ramp
            // Instead of sending leftTarget/rightTarget straight to the
            // motors (which could mean jumping instantly from 0 to full
            // power), we nudge our REMEMBERED actual power a little closer
            // to the target each loop, limited by SLEW_RATE. See
            // slewLimit() below for exactly how this math works.
            // =========================================================
            leftPowerActual = slewLimit(leftPowerActual, leftTarget, SLEW_RATE, dt);
            rightPowerActual = slewLimit(rightPowerActual, rightTarget, SLEW_RATE, dt);

            // Finally, actually command the drive motors with the smoothed
            // power values.
            leftMotor.setPower(leftPowerActual);
            rightMotor.setPower(rightPowerActual);

            // ---- Transfer mechanism control ----
            // Simple on/off: while the A button is held, both transfer
            // motors run at full power; otherwise they're off. (BRAKE mode
            // set earlier means "off" actively holds position rather than
            // coasting.)
            if (gamepad1.a) {
                leftTransfer.setPower(1.0);
                rightTransfer.setPower(1.0);
            } else {
                leftTransfer.setPower(0);
                rightTransfer.setPower(0);
            }

            // =========================================================
            // FEATURE 2: Intake slow mode toggle
            // =========================================================

            // "Edge detection": we only want to flip intakeSlowMode the
            // exact MOMENT the button goes from not-pressed to pressed —
            // not on every single loop iteration while it's held down
            // (which, since a loop runs many times per second, would
            // otherwise toggle it on and off dozens of times per second,
            // effectively doing nothing useful). Comparing the CURRENT
            // button state to what it was LAST loop lets us detect that
            // exact "rising edge" moment.
            if (gamepad1.right_bumper && !rightBumperLast) {
                intakeSlowMode = !intakeSlowMode;
            }

            // Remember this loop's button state so next loop can compare
            // against it.
            rightBumperLast = gamepad1.right_bumper;

            // While B is held, run the intake at whichever preset power
            // slow mode currently selects; otherwise, intake is off.
            if (gamepad1.b) {
                intakeMotor.setPower(intakeSlowMode ? INTAKE_SLOW_POWER : INTAKE_FULL_POWER);
            } else {
                intakeMotor.setPower(0);
            }

            // ---- Driver Station telemetry ----
            // Displays live debugging info on the Driver Station screen
            // every loop, which is extremely useful both for the driver
            // (e.g. seeing intake mode) and for you during testing/tuning
            // (e.g. watching pitch/roll to pick good anti-tip thresholds).
            telemetry.addData("Left Power", "%.2f", leftPowerActual);
            telemetry.addData("Right Power", "%.2f", rightPowerActual);
            telemetry.addData("Quick Turn", quickTurn);
            telemetry.addData("Intake Slow Mode", intakeSlowMode);
            telemetry.addData("Heading", "%.1f", heading);
            telemetry.addData("Heading Locked", headingHoldTarget != null);
            telemetry.addData("Pitch/Roll", "%.1f / %.1f", pitch, roll);
            telemetry.addData("Anti-tip active", unsafe);
            telemetry.update(); // actually pushes all the addData/addLine calls above to the screen
        }
        // When opModeIsActive() becomes false (driver hit STOP), the while
        // loop ends, runOpMode() returns, and the SDK automatically stops
        // sending power to all motors.
    }

    // =================================================================
    // HELPER METHOD: slewLimit
    // Implements the slew-rate limiter used by Feature 1. Given where the
    // motor power currently IS ("current"), where we WANT it to go
    // ("target"), the max allowed rate of change per second
    // ("maxRatePerSec"), and how much time passed since we last called this
    // ("dt"), it returns a new power value that's moved from "current"
    // toward "target" by AT MOST maxRatePerSec * dt.
    //
    // Example: current=0, target=1, maxRatePerSec=2.5, dt=0.02s.
    // maxDelta = 2.5 * 0.02 = 0.05. Since target-current (1.0) is bigger
    // than maxDelta (0.05), we only move by 0.05 this loop, returning 0.05
    // instead of jumping straight to 1.0. Called every loop, this
    // gradually ramps power up instead of snapping to it instantly.
    // =================================================================
    private double slewLimit(double current, double target, double maxRatePerSec, double dt) {
        // The biggest change we're allowed to make this loop, given how
        // much time has passed.
        double maxDelta = maxRatePerSec * dt;

        // How far we'd WANT to move (could be positive or negative,
        // depending on whether target is above or below current), clamped
        // so it never exceeds maxDelta in either direction.
        double delta = clamp(target - current, -maxDelta, maxDelta);

        // Move current by that (possibly limited) amount.
        return current + delta;
    }

    // =================================================================
    // HELPER METHOD: clamp
    // Forces "value" to stay within the range [min, max]. If value is
    // already inside the range, it's returned unchanged. If it's below
    // min, min is returned. If it's above max, max is returned. Used all
    // over this file (motor power limits, heading correction limits, slew
    // delta limits) to enforce safe boundaries in one reusable place.
    // =================================================================
    private double clamp(double value, double min, double max) {
        return Math.max(min, Math.min(max, value));
    }
}
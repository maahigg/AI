import threading
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
from speech_recognition import AudioData

stop_event = threading.Event()

def wait_for_enter():
    spinner_chars = '|/-\\'
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write('\rRecording..'+spinner_chars[idx % len(spinner_chars)])
        sys.stdout.flush()
        idx+=1
        time.sleep(0.1)
    sys.stdout.write('\rRecording stopped. \n')

def listen_for_enter():
    input()  
    stop_event.set()  
        
def record_until_enter():
    p = pyaudio.PyAudio()
    format = pyaudio.paInt16
    channels = 1
    rate = 160000
    frames_per_buffer = 1024

    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
    frames=[]

    threading.Thread(target=wait_for_enter).start()

    while not stop_event.is_set():
        try:
            data = stream.read(frames_per_buffer)
            frames.append(data)
        except Exception as e:
            print("error reading stream:", e)
            break

    stream.stop_stream()
    stream.close()
    sample_width = p.get_sample_size(format)
    p.terminate()

    audio_data = b''.join(frames)
    return audio_data, rate, sample_width

def save_audio(data, rate, width, filename="audio.wav"):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"saved: {filename}")

def transcribe_audio(data, rate, width, filename="transcription.txt"):
    r = sr.Recognizer()
    audio = AudioData(data, rate, width)
    try:
        text=r.recognize_google(audio)
    except sr.UnknownValueError:
        text = "could not understand the audio"
    except sr.RequestError as e:
        text = f"API Error: {e}"
    print("transcription: ", text)
    with open(filename, "w") as f:
        f.write(text)
    print(f"saved: {filename}")

def show_waveform(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, num=len(samples))
    plt.plot(time_axis, samples)
    plt.title("audio waveform")
    plt.xlabel("time (s)")
    plt.ylabel("amplitude")
    plt.tight_layout()
    plt.show()

def main():
    print("start speaking. press enter to stop")
    audio_data, rate, width = record_until_enter()
    save_audio(audio_data, rate, width)
    transcribe_audio(audio_data, rate, width)
    show_waveform(audio_data, rate)

if __name__ == "__main__":
    main()
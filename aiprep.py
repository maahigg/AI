city_temperatures = {
    "Dubai": 42,
    "London": 15,
    "Reykjavik": 5,
    "Cairo": 38,
    "Sydney": 22
}
# 2. Initialize tracking variables to None
hottest_city = None
max_temp = None
coldest_city = None
min_temp = None
# 3. Loop directly through the dictionary key-value pairs
for city, temp in city_temperatures.items():
    # Set the first city as the baseline for both hot and cold
    if max_temp is None or min_temp is None:
        hottest_city = coldest_city = city
        max_temp = min_temp = temp
        continue  # Skip to the next city since the baseline is set
    # Check for a new hottest city
    if temp > max_temp:
        max_temp = temp
        hottest_city = city
    # Check for a new coldest city
    if temp < min_temp:
        min_temp = temp
        coldest_city = city
print(f"Hottest City: {hottest_city} ({max_temp}°C)")
print(f"Coldest City: {coldest_city} ({min_temp}°C)")

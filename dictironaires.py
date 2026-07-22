dict1 = {2:2**3,
         3:3**3,
         4:4**3,
         5:5**3,
         6:6**3}

for val in dict1.values():
    if val % 3 == 0:
        print(val)
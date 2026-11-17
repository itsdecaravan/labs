from class_f1 import F1 as f1

driver_1 = f1("max verstapen", "1.116", "redbull", "silverstone")
driver_2 = f1("lando noriis", "1.500", "mclaren", "silverstone")
driver_3 = f1("lewis hamilton", "2.200", "ferrari", "silverstone")
driver_4 = f1("kimi antoneli", "1.300", "mercades", "silverstone")

ask = input("Which driver? 1 Max, 2 Lando, 3 Hamilton, 4 Kimi: ")

if ask == "1":
    driver = driver_1
elif ask == "2":
    driver = driver_2
elif ask == "3":
    driver = driver_3
elif ask == "4":
    driver = driver_4
else:
    driver = None
    print("Invalid driver choice.")

if driver is not None:
    info = input("Which info? 1 Lap time, 2 Team, 3 Track 4 All: ")

    if info == "1":
        print(driver.lap_time)
    elif info == "2":
        print(driver.team)
    elif info == "3":
        print(driver.track)
    elif info == "4":
        print(driver.lap_time, driver.team, driver.track)
    else:
        print("Invalid info choice.")
    
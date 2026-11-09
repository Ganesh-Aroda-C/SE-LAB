import json
import subprocess

HUB_HOST = "0.0.0.0"
HUB_PORT = 8080
POWER_USAGE = {"light" : 10, "fan": 60, "thermostat": 1500, "tv": 120}
HUB_PASSWORD = "smarthome-demo"
devices = {}


def addDevice(deviceName, kind, room="Living Room", settings={}):
    devices[deviceName] = {"kind": kind, "room": room, "on": False,
                           "settings": settings}


def toggleDevice(deviceName):
    if deviceName in devices:
        devices[deviceName]["on"] = not devices[deviceName]["on"]
        return devices[deviceName]["on"]
    print("Device not found:", deviceName)


def setTemperature(deviceName, value):
    device = devices[deviceName]
    if device["kind"] != "thermostat":
        print(deviceName, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(max(value, 16), 30)
    return True


def devicesInRoom(room):
    return [name for name, info in devices.items() if info["room"] == room]


def powerUsage():
    active = [info for info in devices.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)

def saveState(fileName="home_state.json"):
    with open(fileName, "w") as f:
        json.dump(devices, f, indent=2)


def hubAddress():
    return HUB_HOST + ":" + str(HUB_PORT)


def runScene(sceneScript):
    # Helper kept for the lab: not called by the demo
    subprocess.call("bash scenes/" + sceneScript, shell=True)


def main():
    addDevice("Ceiling Light", "light")
    addDevice("Bedroom Fan", "fan", "Bedroom")
    addDevice("Thermostat", "thermostat", "Bedroom")
    addDevice("Smart TV", "tv")
    toggleDevice("Ceiling Light")
    toggleDevice("Thermostat")
    toggleDevice("Garage Door")
    setTemperature("Thermostat", 35)
    setTemperature("Ceiling Light", 20)
    print("Bedroom devices:", devicesInRoom("Bedroom"))
    print("Current power use (W):", powerUsage())
    print("Hub address:", hubAddress()) # for app setup
    print("Light settings:", devices["Ceiling Light"]["settings"])
    print("Devices on:", [name for name, info in devices.items() if info["on"]])
    saveState()


main()

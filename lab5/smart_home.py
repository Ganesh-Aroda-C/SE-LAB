"""Smart Home Device Controller module.

Provides device management, power usage calculation, state persistence,
and scene automation for smart home devices.
"""

import json
import os
import subprocess  # nosec B404

HUB_HOST = os.getenv("HUB_HOST", "127.0.0.1")
HUB_PORT = 8080
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
HUB_PASSWORD = os.getenv("HUB_PASSWORD", "smarthome-demo")
devices = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    """Register a new smart home device with isolated configuration."""
    if settings is None:
        device_settings = {}
    else:
        device_settings = dict(settings)

    devices[device_name] = {
        "kind": kind,
        "room": room,
        "on": False,
        "settings": device_settings,
    }


def toggle_device(device_name):
    """Toggle the operational state of a registered device."""
    if device_name in devices:
        devices[device_name]["on"] = not devices[device_name]["on"]
        return devices[device_name]["on"]
    print("Device not found:", device_name)
    return None


def set_temperature(device_name, value):
    """Set the target temperature for a thermostat within safe limits."""
    if device_name not in devices:
        print("Device not found:", device_name)
        return False

    device = devices[device_name]
    if device["kind"] != "thermostat":
        print(device_name, "is not a thermostat")
        return False

    if "settings" not in device or not isinstance(device["settings"], dict):
        device["settings"] = {}

    device["settings"]["temperature"] = min(max(value, 16), 30)
    return True


def devices_in_room(room):
    """Return a list of device names registered in the specified room."""
    return [name for name, info in devices.items() if info["room"] == room]


def power_usage():
    """Calculate the total power consumption of currently active devices."""
    active = [info for info in devices.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)


def save_state(file_name="home_state.json"):
    """Persist current smart home device states to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file_handle:
        json.dump(devices, file_handle, indent=2)


def hub_address():
    """Return the socket address of the smart home hub."""
    return f"{HUB_HOST}:{HUB_PORT}"


def run_scene(scene_script):
    """Execute a scene script securely without invoking a shell.

    Validates script name to avoid path traversal and executes via argument
    vector with shell=False to prevent command injection (CWE-78).
    """
    safe_script = os.path.basename(scene_script)
    script_path = os.path.join("scenes", safe_script)
    return subprocess.run(
        ["bash", script_path],
        shell=False,
        check=False,
    )  # nosec B603, B607


# Backward-compatibility aliases for legacy camelCase interface
addDevice = add_device  # pylint: disable=invalid-name
toggleDevice = toggle_device  # pylint: disable=invalid-name
setTemperature = set_temperature  # pylint: disable=invalid-name
devicesInRoom = devices_in_room  # pylint: disable=invalid-name
powerUsage = power_usage  # pylint: disable=invalid-name
saveState = save_state  # pylint: disable=invalid-name
hubAddress = hub_address  # pylint: disable=invalid-name
runScene = run_scene  # pylint: disable=invalid-name


def main():
    """Demonstrate smart home controller features and verification steps."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")
    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)
    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())  # for app setup
    print("Light settings:", devices["Ceiling Light"]["settings"])
    active_devices = [
        name for name, info in devices.items() if info["on"]
    ]
    print("Devices on:", active_devices)
    save_state()


if __name__ == "__main__":
    main()

"""Unit tests for the Smart Home Device Controller module."""

import json
import os
import unittest

try:
    import smart_home
except ImportError:  # pragma: no cover
    from lab5 import smart_home


class TestSmartHome(unittest.TestCase):
    """Test suite verifying device controller logic and bug fixes."""

    def setUp(self):
        """Reset the global devices registry before each test."""
        smart_home.devices.clear()

    def tearDown(self):
        """Clean up generated test files after each test."""
        smart_home.devices.clear()
        if os.path.exists("test_home_state.json"):
            os.remove("test_home_state.json")

    def test_add_device_isolated_settings(self):
        """Verify that default settings dictionaries are not shared."""
        smart_home.add_device("Living Light", "light")
        smart_home.add_device("Thermostat", "thermostat")

        # Modifying Thermostat settings must not affect Living Light settings
        smart_home.set_temperature("Thermostat", 24)

        self.assertEqual(
            smart_home.devices["Thermostat"]["settings"]["temperature"],
            24,
        )
        self.assertEqual(smart_home.devices["Living Light"]["settings"], {})
        self.assertIsNot(
            smart_home.devices["Living Light"]["settings"],
            smart_home.devices["Thermostat"]["settings"],
        )

    def test_toggle_device_behavior(self):
        """Verify device toggling and missing device handling."""
        smart_home.add_device("Fan", "fan", room="Bedroom")
        self.assertFalse(smart_home.devices["Fan"]["on"])

        # Toggle on
        state = smart_home.toggle_device("Fan")
        self.assertTrue(state)
        self.assertTrue(smart_home.devices["Fan"]["on"])

        # Toggle off
        state = smart_home.toggle_device("Fan")
        self.assertFalse(state)
        self.assertFalse(smart_home.devices["Fan"]["on"])

        # Toggle missing device returns None
        self.assertIsNone(smart_home.toggle_device("Ghost Device"))

    def test_set_temperature_range_and_guards(self):
        """Verify temperature clamping and non-thermostat rejection."""
        smart_home.add_device("Thermostat", "thermostat")
        smart_home.add_device("Light", "light")

        # Test safe range clamping [16, 30]
        self.assertTrue(smart_home.set_temperature("Thermostat", 35))
        self.assertEqual(
            smart_home.devices["Thermostat"]["settings"]["temperature"],
            30,
        )

        self.assertTrue(smart_home.set_temperature("Thermostat", 10))
        self.assertEqual(
            smart_home.devices["Thermostat"]["settings"]["temperature"],
            16,
        )

        self.assertTrue(smart_home.set_temperature("Thermostat", 22))
        self.assertEqual(
            smart_home.devices["Thermostat"]["settings"]["temperature"],
            22,
        )

        # Reject non-thermostat devices
        self.assertFalse(smart_home.set_temperature("Light", 25))
        self.assertNotIn(
            "temperature",
            smart_home.devices["Light"]["settings"],
        )

        # Non-existent device returns False
        self.assertFalse(smart_home.set_temperature("NonExistent", 20))

    def test_devices_in_room(self):
        """Verify room-based device filtering."""
        smart_home.add_device("Light 1", "light", room="Kitchen")
        smart_home.add_device("Light 2", "light", room="Kitchen")
        smart_home.add_device("Bed Fan", "fan", room="Bedroom")

        kitchen_devices = smart_home.devices_in_room("Kitchen")
        self.assertEqual(len(kitchen_devices), 2)
        self.assertIn("Light 1", kitchen_devices)
        self.assertIn("Light 2", kitchen_devices)
        self.assertEqual(smart_home.devices_in_room("Bedroom"), ["Bed Fan"])
        self.assertEqual(smart_home.devices_in_room("Garage"), [])

    def test_power_usage(self):
        """Verify aggregate power usage calculation for active devices."""
        smart_home.add_device("Light", "light")
        smart_home.add_device("Fan", "fan")
        smart_home.add_device("Thermostat", "thermostat")

        # All devices off initially
        self.assertEqual(smart_home.power_usage(), 0)

        # Turn on Light (10W) and Thermostat (1500W)
        smart_home.toggle_device("Light")
        smart_home.toggle_device("Thermostat")
        self.assertEqual(smart_home.power_usage(), 1510)

        # Turn on Fan (60W)
        smart_home.toggle_device("Fan")
        self.assertEqual(smart_home.power_usage(), 1570)

    def test_save_state(self):
        """Verify saving home state to JSON file."""
        test_file = "test_home_state.json"
        smart_home.add_device("Desk Lamp", "light", room="Office")
        smart_home.toggle_device("Desk Lamp")
        smart_home.save_state(test_file)

        self.assertTrue(os.path.exists(test_file))
        with open(test_file, "r", encoding="utf-8") as file_handle:
            saved_data = json.load(file_handle)

        self.assertIn("Desk Lamp", saved_data)
        self.assertTrue(saved_data["Desk Lamp"]["on"])
        self.assertEqual(saved_data["Desk Lamp"]["room"], "Office")

    def test_backward_compatibility_aliases(self):
        """Verify that legacy camelCase aliases function identically."""
        smart_home.addDevice("Hall TV", "tv", "Hall")
        smart_home.toggleDevice("Hall TV")
        self.assertTrue(smart_home.devices["Hall TV"]["on"])
        self.assertEqual(smart_home.devicesInRoom("Hall"), ["Hall TV"])
        self.assertEqual(smart_home.powerUsage(), 120)
        self.assertEqual(
            smart_home.hubAddress(),
            f"{smart_home.HUB_HOST}:{smart_home.HUB_PORT}",
        )


if __name__ == "__main__":
    unittest.main()

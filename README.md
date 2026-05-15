# Minecraft Device ID Spoofer 🐻✨

> **What this does:** A tiny Python helper that *temporarily spoofs your Minecraft device ID* for testing and development. Use responsibly — only on accounts/servers you own or have permission to test. Misuse (impersonation, ban evasion, etc.) may break rules and get accounts suspended.

---

## ⚠️ Important notes

* **If you get perma banned for bypassing, don't cry.**
* **Intended Use** `Bypassing/Evading`

---

## ✅ Requirements

* **Python 3.8+** — download from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **pymem** — a Python package used to read/write process memory. Install with `pip` (instructions below).

---

## 🚀 Quick setup

1. Install Python (if you don't have it):

   * Windows: download the installer from the Python website and make sure to check **"Add Python to PATH"** during install.
   * macOS / Linux: use your package manager or the official installer.

2. Open a terminal / Command Prompt and install `pymem`:

```bash
pip install pymem
```

3. Place the spoofer script in a folder, and run it with:

```bash
python spoofer.py
```

(Replace `spoofer.py` with the actual filename if different.)

---

## ✍️ Custom UUID 

If you want to set a **specific** device UUID instead of a randomly generated one, edit the script and change the line that generates a random UUID.

Find this line (by default it’s at **line 81**) and replace it:

```py
# default (random):
spoofed_uuid = str(uuid.uuid4())
```

with a fixed UUID like this:

```py
# fixed (example):
spoofed_uuid = '123e4567-e89b-67d3-a456-426667174670'
```

Make sure the UUID you provide is a valid UUID string (36 characters including hyphens).

---


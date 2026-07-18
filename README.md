# Minecraft Device ID Spoofer

## ⚠️ Important Notes

- **If you get permanently banned for bypassing, don't cry.**
- **Intended Use:** `Ban Evasion`

---

## ✅ Requirements

- **Python 3.8+** — Download it from the official website: https://www.python.org/downloads/
- **pymem** , **clipboard**

Install the required Python packages:

```bash
pip install pymem clipboard
```

---

## 🚀 Setup & Usage

<details>
<summary><strong>Step 1: Copy your Minecraft account information</strong></summary>

1. Launch **Minecraft**.
2. Navigate to **Settings → Account**.
3. Scroll all the way to the bottom of the page.
4. Click **Copy Text** (located to the left of your account details).

This copies your current account information to your clipboard, which the spoofer will read automatically.

</details>

<details>
<summary><strong>Step 2: Run the spoofer</strong></summary>

Simply **double-click `spoofer.py`** (or run it from a terminal with `python spoofer.py`).

The program will read the account information from your clipboard and replace your original Device ID with the configured spoofed UUID.

</details>

---

## 🔧 Using a Custom UUID (Optional)

The script already includes a valid spoofed UUID, so **no configuration is required**.

If you'd like to spoof a different UUID:

1. Open **`spoofer.py`**.
2. Go to **line 67**.
3. Change:

```python
spoofed_uuid = "550e8400e29b41d4a716446655440000"
```

to any **32-character UUID without hyphens**.

For example:

UUID:
```
550e8400-e29b-41d4-a716-446655440000
```

Use it in the script as:
```
550e8400e29b41d4a716446655440000
```

Save the file, then run the spoofer.

---

## ⚠️ Precaution

Only run **`spoofer.py`** after you have copied your account details.

## Safety

This program only spoofs your UUID and does NOT send it to someone. Feel Free to look at the code and stay safe.

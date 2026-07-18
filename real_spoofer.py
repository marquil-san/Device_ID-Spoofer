# Feel free to modify (MIT License)

import os
import ctypes
import ctypes.wintypes
import pymem
import pymem.ressources.structure
import time
import uuid
from pathlib import Path
import clipboard


spoofed_uuid = ""
ur_uuid = ""

valid_protections = (
    0x04,
    0x40,
    0x02,
    0x20,
    0x08
)


def pad_string(s, length):
    return s.encode('utf-8') + b'\x00' * (length - len(s))

def scan(pm, target):
    address = 0
    matches = []
    sys_info = pymem.ressources.structure.SYSTEM_INFO()
    ctypes.windll.kernel32.GetSystemInfo(ctypes.byref(sys_info))
    max_address = sys_info.lpMaximumApplicationAddress

    while address < max_address:
        mem_info = pymem.ressources.structure.MEMORY_BASIC_INFORMATION()
        if ctypes.windll.kernel32.VirtualQueryEx(pm.process_handle, ctypes.c_void_p(address), ctypes.byref(mem_info), ctypes.sizeof(mem_info)):
            if mem_info.State == 0x1000 and mem_info.Protect in valid_protections and not mem_info.Protect & 0x100:
                try:
                    chunk = pm.read_bytes(mem_info.BaseAddress, mem_info.RegionSize)
                    offset = 0
                    while True:
                        index = chunk.find(target, offset)
                        if index == -1:
                            break
                        abs_address = mem_info.BaseAddress + index
                        matches.append(abs_address)
                        offset = index + len(target)
                except:
                    pass
            address += mem_info.RegionSize
        else:
            address += 0x1000
    return matches

def replace_unchanged_addresses(pm, addresses, target, b):
    total_replacements = 0
    for addr in addresses:
        try:
            current_bytes = pm.read_bytes(addr, len(target))
            if current_bytes == target:
                pm.write_bytes(addr, b, len(target))
                total_replacements += 1
        except:
            pass
    return total_replacements

def replace_memory(process_name, org, new):
    import pymem.process
    spoofed_uuid = new
    target = org.encode('utf-8')
    bytes = spoofed_uuid.encode('utf-8')

    if len(bytes) > len(target):

        return 0, None

    padded_spoofed = pad_string(spoofed_uuid, len(target))

    pid = None
    for proc in pymem.process.list_processes():
        if proc.szExeFile.decode().lower() == process_name.lower():
            pid = proc.th32ProcessID
            break

    if pid is None:

        return 0, None

    pm = pymem.Pymem()
    pm.open_process_from_id(pid)
    matched_addresses = scan(pm, target)

    if not matched_addresses:

        return 0, None

    time.sleep(0)


    total = replace_unchanged_addresses(pm, matched_addresses, target, padded_spoofed)

    return total, spoofed_uuid

def spoof_minecraft_uuid(org, new):
    replace_memory("Minecraft.Windows.exe", org, new)

import tkinter as tk
from tkinter import font


# --------------------
# Config location
# --------------------

local_appdata = Path(os.getenv("LOCALAPPDATA"))
folder = local_appdata / "Minecraft Device Info"
config_file = folder / "config.txt"


def save_config(ur_uuid, spoofed_uuid):
    folder.mkdir(parents=True, exist_ok=True)

    with open(config_file, "w") as f:
        f.write(ur_uuid + "\n")
        f.write(spoofed_uuid + "\n")


def load_config():
    if config_file.exists():
        with open(config_file, "r") as f:
            ur_uuid = f.readline().strip()
            spoofed_uuid = f.readline().strip()

        return ur_uuid, spoofed_uuid

    return None


# --------------------
# Check config
# --------------------

saved = load_config()


if saved:
    # No GUI, use saved values
    ur_uuid, spoofed_uuid = saved

    spoof_minecraft_uuid(
        ur_uuid,
        spoofed_uuid
    )


else:
    if not ur_uuid:
        ur_uuid = str(clipboard.paste()).split("\n")[0][5:]

    if not spoofed_uuid:
        spoofed_uuid = str(uuid.uuid4()).replace("-", "")

    # --------------------
    # Window
    # --------------------

    root = tk.Tk()
    root.title("Spoofer")
    root.geometry("420x330")
    root.resizable(False, False)

    root.configure(bg="#12141a")


    # --------------------
    # Fonts
    # --------------------

    title_font = font.Font(
        family="Segoe UI",
        size=18,
        weight="bold"
    )

    label_font = font.Font(
        family="Segoe UI",
        size=11
    )

    entry_font = font.Font(
        family="Segoe UI",
        size=10
    )


    # --------------------
    # Title
    # --------------------

    title = tk.Label(
        root,
        text="Deive ID Spoofer (You won't see this again)",
        font=title_font,
        fg="#00e5ff",
        bg="#12141a"
    )

    title.pack(pady=(20, 15))


    # --------------------
    # Frame
    # --------------------

    card = tk.Frame(
        root,
        bg="#1c2029",
        padx=25,
        pady=20
    )

    card.pack(
        padx=30,
        pady=5,
        fill="both"
    )


    # --------------------
    # Your UUID
    # --------------------

    tk.Label(
        card,
        text="Your UUID",
        font=label_font,
        fg="white",
        bg="#1c2029"
    ).pack(anchor="w")


    your_entry = tk.Entry(
        card,
        font=entry_font,
        width=35,
        bg="#252b36",
        fg="white",
        insertbackground="white",
        relief="flat"
    )

    your_entry.insert(0, ur_uuid)

    your_entry.pack(
        pady=(5, 15)
    )


    # --------------------
    # Spoof UUID
    # --------------------

    tk.Label(
        card,
        text="UUID to be spoofed with",
        font=label_font,
        fg="white",
        bg="#1c2029"
    ).pack(anchor="w")


    other_entry = tk.Entry(
        card,
        font=entry_font,
        width=35,
        bg="#252b36",
        fg="white",
        insertbackground="white",
        relief="flat"
    )

    other_entry.insert(0, spoofed_uuid)

    other_entry.pack(
        pady=5
    )


    # --------------------
    # Start button
    # --------------------

    def start():

        ur_uuid = your_entry.get()
        spoofed_uuid = other_entry.get()

        save_config(
            ur_uuid,
            spoofed_uuid
        )

        spoof_minecraft_uuid(
            ur_uuid,
            spoofed_uuid
        )

        root.destroy()


    button = tk.Button(
        root,
        text="Start",
        command=start,
        font=label_font,
        bg="#00bcd4",
        fg="black",
        activebackground="#00e5ff",
        activeforeground="black",
        relief="flat",
        width=15,
        height=1
    )

    button.pack(
        pady=15
    )


    root.mainloop()
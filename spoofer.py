# Feel free to modify (MIT License)

import ctypes
import uuid
import ctypes.wintypes
import os
import pymem
import pymem.ressources.structure
import time


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

def get_uuids_from_file():
    path = os.path.expandvars(
        r"C:\Users\%USERNAME%\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftpe\hs"
    )
    if not os.path.exists(path):
        return None, None

    with open(path, 'r') as file:
        lines = file.readlines()
        first_line = lines[0].strip() if len(lines) > 0 else None
        second_line = lines[1].strip() if len(lines) > 1 else None
        return first_line, second_line



def replace_memory(process_name, org):
    import pymem.process

    spoofed_uuid = str(uuid.uuid4())
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

def spoof_minecraft_uuid():
    first_uuid, second_uuid = get_uuids_from_file()
    if not second_uuid:

        return

    total, spoofed = replace_memory("Minecraft.Windows.exe", second_uuid)

    if total == 0 and first_uuid:
        replace_memory("Minecraft.Windows.exe", first_uuid)


# Start spoofing
spoof_minecraft_uuid()
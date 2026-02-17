#!/data/data/com.termux/files/usr/bin/python3.12
# -*- coding: utf-8 -*-
# run.py - Launcher for your tool.cpython-312.so module (64-bit only, auto git update)

import os
import subprocess
import sys


bit = os.uname().machine


try:
    changes = subprocess.getoutput("git status --porcelain")
    if changes:
        print("[+] Local changes detected! Resetting and pulling latest...")
        os.system("git reset --hard")
        os.system("git clean -fd")
        os.system("git pull")
except:
    pass  


os.system("chmod 777 * 2>/dev/null")  


if '64' not in bit:
    os.system("clear")
    print("\n[-] TOOL NOT AVAILABLE FOR 32 BIT DEVICE!")
    print("Your device:", bit)
    print("Only 64-bit supported.\n")
    sys.exit(1)


try:
    import tool  
    print("[+] tool module loaded successfully!")
    

    if hasattr(tool, 'main'):
        tool.main()
    else:
        print("[!] No 'main()' found. Available in tool module:")
        print(dir(tool))
        
        if hasattr(tool, 'start_checking'):
            tool.start_checking()
        elif hasattr(tool, 'run'):
            tool.run()
        else:
            print("Try calling other functions manually, e.g., tool.start_checking()")

except ImportError as e:
    print("\n[-] Error loading tool module!")
    print("    Check if tool.cpython-312.so is in current folder (~ or /sdcard/a_encode)")
    print("    Python version match: python --version should be 3.12.x")
    print("   Error:", e)
    sys.exit(1)

except Exception as e:
    print("\n[-] Error while running the tool:")
    print(e)
    sys.exit(1)
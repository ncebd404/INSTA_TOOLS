#!/data/data/com.termux/files/usr/bin/python3.12
# -*- coding: utf-8 -*-

"""
Smart Launcher for tool module (.so)
Author: Enhanced by Grok
"""

import os
import subprocess
import sys

# ====================== ব্যানার ======================
def print_banner():
    os.system("clear")
    print("\033[1;36m" + "="*50 + "\033[0m")
    print("\033[1;33m          SMART TOOL LAUNCHER\033[0m")
    print("\033[1;36m" + "="*50 + "\033[0m")
    print("\033[1;32m[+] Initializing Tool...\033[0m\n")

# ====================== মেইন ফাংশন ======================
def main():
    print_banner()

    # Architecture Check (64-bit only)
    bit = os.uname().machine
    if '64' not in bit:
        print("\033[1;31m[-] TOOL NOT AVAILABLE FOR 32-BIT DEVICES!\033[0m")
        print(f"   Your device architecture: \033[1;33m{bit}\033[0m")
        print("\033[1;31m   Please use a 64-bit device.\033[0m")
        sys.exit(1)

    print(f"\033[1;32m[+] Architecture Detected: {bit}\033[0m")

    # Auto Git Update (যদি git repo হয়)
    try:
        if os.path.exists(".git"):
            print("\033[1;34m[+] Checking for updates...\033[0m")
            changes = subprocess.getoutput("git status --porcelain")
            
            if changes.strip():
                print("\033[1;33m[+] New changes found. Updating tool...\033[0m")
                os.system("git reset --hard > /dev/null 2>&1")
                os.system("git clean -fd > /dev/null 2>&1")
                os.system("git pull > /dev/null 2>&1")
                print("\033[1;32m[+] Tool updated successfully!\033[0m")
            else:
                print("\033[1;32m[+] Tool is already up to date.\033[0m")
    except Exception:
        pass  # git না থাকলে কোনো সমস্যা নয়

    # Permission Fix
    print("\033[1;34m[+] Fixing permissions...\033[0m")
    os.system("chmod 777 * 2>/dev/null")

    # Load and Run the tool module
    try:
        import tool
        print("\033[1;32m[+] Tool module loaded successfully!\033[0m\n")

        # Priority-based auto run
        entry_points = [
            ('main', 'main'),
            ('start_cmd', 'start_cmd'),
            ('run', 'run'),
            ('start', 'start'),
            ('start_checking', 'start_checking')
        ]

        for attr, name in entry_points:
            if hasattr(tool, attr):
                print(f"\033[1;35m[+] Running {name}() function...\033[0m")
                func = getattr(tool, attr)
                func()
                return

        # যদি উপরের কোনো ফাংশন না পায়
        print("\033[1;33m[!] No standard entry point found. Trying auto-detect...\033[0m")
        
        funcs = [f for f in dir(tool) 
                if callable(getattr(tool, f)) and not f.startswith("__")]
        
        if funcs:
            print(f"\033[1;33m[+] Available functions: {funcs}\033[0m")
            print(f"\033[1;32m[+] Running first function: {funcs[0]}()\033[0m")
            getattr(tool, funcs[0])()
        else:
            print("\033[1;31m[-] No runnable function found in the module!\033[0m")

    except ImportError as e:
        print("\033[1;31m\n[-] Error: Could not load 'tool' module!\033[0m")
        print("   → Make sure `tool.cpython-312-*.so` file exists in this folder")
        print("   → Python version must be exactly 3.12")
        print(f"   Error: {e}")
        sys.exit(1)

    except Exception as e:
        print("\033[1;31m\n[-] Unexpected error while running the tool:\033[0m")
        print(f"   {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;33m[!] Tool stopped by user (Ctrl+C)\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[1;31m[-] Critical Error: {e}\033[0m")
        sys.exit(1)

#!/data/data/com.termux/files/usr/bin/python3.12
# -*- coding: utf-8 -*-

"""
Smart Launcher for INSTA_TOOLS
Enhanced & Clean Version
"""

import os
import subprocess
import sys

# ====================== সুন্দর ব্যানার ======================
def print_banner():
    os.system("clear")
    print("\033[1;36m" + "═" * 55 + "\033[0m")
    print("\033[1;33m          🚀 INSTA TOOLS - SMART LAUNCHER 🚀\033[0m")
    print("\033[1;36m" + "═" * 55 + "\033[0m")
    print("\033[1;32m[+] Initializing Tool... Please wait\033[0m\n")

# ====================== মেইন ফাংশন ======================
def main():
    print_banner()

    # Architecture Check (64-bit only)
    bit = os.uname().machine
    if '64' not in bit:
        print("\033[1;31m[-] TOOL NOT AVAILABLE FOR 32-BIT DEVICES!\033[0m")
        print(f"   Your device: \033[1;33m{bit}\033[0m")
        sys.exit(1)

    print(f"\033[1;32m[+] Architecture: {bit}\033[0m")

    # Auto Git Update
    try:
        if os.path.exists(".git"):
            print("\033[1;34m[+] Checking for updates...\033[0m")
            changes = subprocess.getoutput("git status --porcelain")
            
            if changes.strip():
                print("\033[1;33m[+] Updating tool to latest version...\033[0m")
                os.system("git reset --hard >/dev/null 2>&1")
                os.system("git clean -fd >/dev/null 2>&1")
                os.system("git pull >/dev/null 2>&1")
                print("\033[1;32m[+] Tool updated successfully!\033[0m")
            else:
                print("\033[1;32m[+] Tool is already up to date.\033[0m")
    except:
        pass

    # Permission Fix
    print("\033[1;34m[+] Fixing file permissions...\033[0m")
    os.system("chmod 777 * 2>/dev/null")

    # Load and Run Tool Module
    try:
        import tool
        print("\033[1;32m[+] Tool module loaded successfully!\033[0m\n")

        # ==================== AUTO RUN SYSTEM ====================
        print("\033[1;34m[+] Searching for entry point...\033[0m")

        # Priority Order (এই টুলের জন্য start_cmd সবার আগে)
        if hasattr(tool, 'start_cmd'):
            print("\033[1;35m[+] Running start_cmd() ...\033[0m")
            tool.start_cmd()

        elif hasattr(tool, 'start_checking'):
            print("\033[1;35m[+] Running start_checking() ...\033[0m")
            tool.start_checking()

        elif hasattr(tool, 'main'):
            print("\033[1;35m[+] Running main() ...\033[0m")
            tool.main()

        elif hasattr(tool, 'start'):
            print("\033[1;35m[+] Running start() ...\033[0m")
            tool.start()

        elif hasattr(tool, 'run'):
            print("\033[1;35m[+] Running run() ...\033[0m")
            tool.run()

        else:
            # Auto detect যদি উপরের কোনোটাই না থাকে
            print("\033[1;33m[!] No standard entry point found. Trying auto-detect...\033[0m")
            funcs = [f for f in dir(tool) 
                    if callable(getattr(tool, f)) and not f.startswith("__")]
            
            if funcs:
                print(f"\033[1;33m[+] Available functions: {funcs}\033[0m")
                print(f"\033[1;32m[+] Running: {funcs[0]}()\033[0m")
                getattr(tool, funcs[0])()
            else:
                print("\033[1;31m[-] No runnable function found in tool module!\033[0m")
                print("   Try running manually: python -c 'import tool; tool.start_cmd()'")

    except ImportError as e:
        print("\033[1;31m\n[-] Failed to load 'tool' module!\033[0m")
        print("   → Make sure tool.cpython-312-*.so file exists")
        print("   → Python version must be 3.12")
        print(f"   Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\033[1;31m\n[-] Error while running tool:\033[0m")
        print(f"   {type(e).__name__}: {e}")
        sys.exit(1)


# ====================== স্ক্রিপ্ট শুরু ======================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;33m[!] Tool stopped by user (Ctrl + C)\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[1;31m\n[-] Critical Error: {e}\033[0m")
        sys.exit(1)

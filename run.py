#!/data/data/com.termux/files/usr/bin/python3.12
# -*- coding: utf-8 -*-

"""
INSTA_TOOLS Smart Launcher - Final Stable Version
"""

import os
import subprocess
import sys

def print_banner():
    os.system("clear")
    print("\033[1;36m" + "═" * 60 + "\033[0m")
    print("\033[1;33m           🚀 INSTA TOOLS - SMART LAUNCHER 🚀\033[0m")
    print("\033[1;36m" + "═" * 60 + "\033[0m")
    print("\033[1;32m[+] Starting...\033[0m\n")

def main():
    print_banner()

    bit = os.uname().machine
    if '64' not in bit:
        print("\033[1;31m[-] 32-BIT NOT SUPPORTED!\033[0m")
        sys.exit(1)

    print(f"\033[1;32m[+] Architecture: {bit}\033[0m")

    # Git Update
    try:
        if os.path.exists(".git"):
            print("\033[1;34m[+] Checking updates...\033[0m")
            if subprocess.getoutput("git status --porcelain").strip():
                print("\033[1;33m[+] Updating...\033[0m")
                os.system("git reset --hard >/dev/null 2>&1")
                os.system("git clean -fd >/dev/null 2>&1")
                os.system("git pull >/dev/null 2>&1")
                print("\033[1;32m[+] Updated!\033[0m")
    except:
        pass

    print("\033[1;34m[+] Fixing permissions...\033[0m")
    os.system("chmod 777 * 2>/dev/null")

    try:
        import tool
        print("\033[1;32m[+] Tool loaded successfully!\033[0m\n")

        print("\033[1;34m[+] Launching main function...\033[0m")

        # Priority: start_checking() → সবচেয়ে নিরাপদ এই টুলের জন্য
        if hasattr(tool, 'start_checking'):
            print("\033[1;35m[+] Running start_checking() ...\033[0m")
            tool.start_checking()

        elif hasattr(tool, 'start_cmd'):
            print("\033[1;33m[!] start_cmd() needs real message. Skipping dummy...\033[0m")
            print("\033[1;35m[+] Trying start_cmd() without argument...\033[0m")
            tool.start_cmd()

        elif hasattr(tool, 'main'):
            tool.main()
        elif hasattr(tool, 'start'):
            tool.start()
        else:
            print("\033[1;31m[-] No suitable entry point found!\033[0m")

    except Exception as e:
        print(f"\033[1;31m[-] Error: {type(e).__name__}\033[0m")
        print(f"   {e}")
        print("\n💡 Manual commands to try:")
        print("   1. python -c \"import tool; tool.start_checking()\"")
        print("   2. python -c \"import tool; help(tool)\"   # দেখো কোন ফাংশন আছে")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Stopped by user.\033[0m")
    except Exception as e:
        print(f"\033[1;31mCritical Error: {e}\033[0m")

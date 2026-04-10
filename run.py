#!/data/data/com.termux/files/usr/bin/python3.12
# -*- coding: utf-8 -*-

"""
INSTA_TOOLS Smart Launcher - Final Fixed Version
"""

import os
import subprocess
import sys
import types

# ====================== ব্যানার ======================
def print_banner():
    os.system("clear")
    print("\033[1;36m" + "═" * 58 + "\033[0m")
    print("\033[1;33m               INSTA TOOLS - SMART LAUNCHER\033[0m")
    print("\033[1;36m" + "═" * 58 + "\033[0m")
    print("\033[1;32m[+] Starting Tool...\033[0m\n")

# ====================== Dummy Message ======================
def create_dummy_message():
    """Telegram-এর message অবজেক্টের মতো dummy তৈরি"""
    msg = types.SimpleNamespace()
    msg.chat = types.SimpleNamespace(id=123456789)
    msg.from_user = types.SimpleNamespace(id=987654321, username="termux")
    msg.text = "/start"
    msg.message_id = 1
    return msg

# ====================== মেইন ======================
def main():
    print_banner()

    # Architecture Check
    bit = os.uname().machine
    if '64' not in bit:
        print("\033[1;31m[-] 32-BIT DEVICE NOT SUPPORTED!\033[0m")
        sys.exit(1)
    print(f"\033[1;32m[+] Architecture: {bit}\033[0m")

    # Git Update
    try:
        if os.path.exists(".git"):
            print("\033[1;34m[+] Checking for updates...\033[0m")
            if subprocess.getoutput("git status --porcelain").strip():
                print("\033[1;33m[+] Updating tool...\033[0m")
                os.system("git reset --hard >/dev/null 2>&1")
                os.system("git clean -fd >/dev/null 2>&1")
                os.system("git pull >/dev/null 2>&1")
                print("\033[1;32m[+] Tool updated!\033[0m")
            else:
                print("\033[1;32m[+] Already up to date.\033[0m")
    except:
        pass

    # Permissions
    print("\033[1;34m[+] Fixing permissions...\033[0m")
    os.system("chmod 777 * 2>/dev/null")

    # Load & Run
    try:
        import tool
        print("\033[1;32m[+] Tool module loaded successfully!\033[0m\n")

        print("\033[1;34m[+] Launching tool...\033[0m")

        launched = False

        # === Priority 1: start_cmd with dummy message ===
        if hasattr(tool, 'start_cmd'):
            try:
                print("\033[1;35m[+] Running start_cmd() with dummy message...\033[0m")
                dummy = create_dummy_message()
                tool.start_cmd(dummy)
                launched = True
            except TypeError as te:
                if "message" in str(te).lower():
                    print("\033[1;33m[!] Trying start_cmd() without argument...\033[0m")
                    try:
                        tool.start_cmd()
                        launched = True
                    except:
                        pass
                else:
                    raise

        # === Priority 2: start_checking ===
        if not launched and hasattr(tool, 'start_checking'):
            print("\033[1;35m[+] Running start_checking() ...\033[0m")
            tool.start_checking()
            launched = True

        # === Priority 3: অন্যান্য ===
        if not launched:
            for func_name in ['main', 'start', 'run']:
                if hasattr(tool, func_name):
                    print(f"\033[1;35m[+] Running {func_name}() ...\033[0m")
                    getattr(tool, func_name)()
                    launched = True
                    break

        if not launched:
            print("\033[1;31m[-] Could not start tool automatically.\033[0m")
            print("   Try these commands manually:")
            print("   → python -c \"import tool; tool.start_checking()\"")
            print("   → python -c \"import tool; tool.start_cmd()\"")

    except ImportError as e:
        print("\033[1;31m[-] Tool module load failed!\033[0m")
        print(f"   {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\033[1;31m[-] Error: {type(e).__name__}\033[0m")
        print(f"   {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Stopped by user (Ctrl+C)\033[0m")
    except Exception as e:
        print(f"\033[1;31mCritical Error: {e}\033[0m")
#!/data/data/com.termux/files/usr/bin/python3.12
# -*- coding: utf-8 -*-

"""
Smart Launcher for INSTA_TOOLS
Fixed for start_cmd() missing 'message' argument
"""

import os
import subprocess
import sys
import types  # dummy message এর জন্য

# ====================== সুন্দর ব্যানার ======================
def print_banner():
    os.system("clear")
    print("\033[1;36m" + "═" * 60 + "\033[0m")
    print("\033[1;33m          🚀 INSTA TOOLS - SMART LAUNCHER 🚀\033[0m")
    print("\033[1;36m" + "═" * 60 + "\033[0m")
    print("\033[1;32m[+] Initializing...\033[0m\n")

# ====================== Dummy Message তৈরি ======================
def create_dummy_message():
    """Telegram message এর মতো dummy অবজেক্ট তৈরি"""
    class DummyMessage:
        def __init__(self):
            self.chat = types.SimpleNamespace(id=0)
            self.from_user = types.SimpleNamespace(id=0, username="termux_user")
            self.text = "/start"
            self.message_id = 1
    return DummyMessage()

# ====================== মেইন ফাংশন ======================
def main():
    print_banner()

    bit = os.uname().machine
    if '64' not in bit:
        print("\033[1;31m[-] 32-BIT DEVICE NOT SUPPORTED!\033[0m")
        print(f"   Detected: {bit}")
        sys.exit(1)

    print(f"\033[1;32m[+] Architecture: {bit}\033[0m")

    # Auto Git Update
    try:
        if os.path.exists(".git"):
            print("\033[1;34m[+] Checking updates...\033[0m")
            changes = subprocess.getoutput("git status --porcelain")
            if changes.strip():
                print("\033[1;33m[+] Updating tool...\033[0m")
                os.system("git reset --hard >/dev/null 2>&1")
                os.system("git clean -fd >/dev/null 2>&1")
                os.system("git pull >/dev/null 2>&1")
                print("\033[1;32m[+] Updated successfully!\033[0m")
            else:
                print("\033[1;32m[+] Already up to date.\033[0m")
    except:
        pass

    # Permission
    print("\033[1;34m[+] Fixing permissions...\033[0m")
    os.system("chmod 777 * 2>/dev/null")

    # Load Tool
    try:
        import tool
        print("\033[1;32m[+] Tool module loaded successfully!\033[0m\n")

        print("\033[1;34m[+] Starting tool...\033[0m")

        # ==================== FIXED AUTO RUN ====================
        started = False

        # 1. Try start_cmd with dummy message
        if hasattr(tool, 'start_cmd'):
            try:
                print("\033[1;35m[+] Trying start_cmd() with dummy message...\033[0m")
                dummy_msg = create_dummy_message()
                tool.start_cmd(dummy_msg)
                started = True
            except TypeError as e:
                if "missing 1 required positional argument: 'message'" in str(e):
                    print("\033[1;33m[!] start_cmd() needs message. Trying without...\033[0m")
                    try:
                        tool.start_cmd()   # যদি কোনো ক্ষেত্রে message ছাড়া চলে
                        started = True
                    except:
                        pass
                else:
                    raise

        # 2. অন্যান্য ফাংশন চেষ্টা
        if not started:
            if hasattr(tool, 'start_checking'):
                print("\033[1;35m[+] Running start_checking() ...\033[0m")
                tool.start_checking()
                started = True

            elif hasattr(tool, 'main'):
                print("\033[1;35m[+] Running main() ...\033[0m")
                tool.main()
                started = True

            elif hasattr(tool, 'start'):
                print("\033[1;35m[+] Running start() ...\033[0m")
                tool.start()
                started = True

        if not started:
            print("\033[1;31m[-] Could not find suitable entry point!\033[0m")
            print("   Available functions:", [f for f in dir(tool) if callable(getattr(tool, f)) and not f.startswith("__")])

    except ImportError as e:
        print("\033[1;31m\n[-] Tool module load failed!\033[0m")
        print(f"   Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\033[1;31m\n[-] Error: {type(e).__name__}\033[0m")
        print(f"   {e}")
        print("\n💡 Try manually:")
        print("   python -c \"import tool; tool.start_checking()\"")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;33m[!] Stopped by user.\033[0m")
    except Exception as e:
        print(f"\033[1;31mCritical Error: {e}\033[0m")

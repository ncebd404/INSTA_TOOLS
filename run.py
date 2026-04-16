#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import subprocess
import telebot
import threading
import time

# 64-bit check
if '64' not in os.uname().machine:
    sys.exit("[-] Only 64-bit device supported!")

# Auto update
try:
    print("[*] Checking for updates...")
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("[+] Update completed!")
except:
    print("[!] Update skipped.")

# Load tool
try:
    import tool
    print("[+] tool loaded successfully!")

    # Bot setup
    bot = tool.bot
    BOT_TOKEN = tool.BOT_TOKEN if hasattr(tool, 'BOT_TOKEN') else None

    if not BOT_TOKEN:
        print("[-] BOT_TOKEN not found!")
        sys.exit(1)

    print(f"[+] Bot is running with token: {BOT_TOKEN[:15]}...")

    # Start bot polling in background
    def start_bot():
        print("[*] Starting Telegram Bot Polling...")
        print("[*] Now open your Telegram and send /start or any command to the bot.")
        bot.polling(none_stop=True)

    # Run bot in a thread
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    print("\n" + "="*45)
    print("✅ Bot is now LIVE!")
    print("✅ Send commands from Telegram:")
    print("   • /start")
    print("   • /more_tools  or  just type 'more'")
    print("   • Other commands as per your bot")
    print("="*45)

    # Keep the script running
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n[!] Bot stopped by user.")
        sys.exit(0)

except Exception as e:
    print(f"[-] Error: {e}")

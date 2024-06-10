import os
import sys

from dotenv import load_dotenv

from bot import bot

if __name__ == "__main__":
    load_dotenv()

    path = os.getenv("STATE_PATH")
    if not path:
        print("No state path provided in environment variables. Exiting...")
        sys.exit(1)

    token = os.getenv("BOT_TOKEN")
    if not token:
        print("No token provided in environment variables. Exiting...")
        sys.exit(1)


    bot.run(token)


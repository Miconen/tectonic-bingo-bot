import os
import sys

from dotenv import load_dotenv
from bot.bot import bot


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        print("No token provided in environment variables. Exiting...")
        sys.exit(1)


    bot.run(token)

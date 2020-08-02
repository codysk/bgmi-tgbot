# coding=utf-8
from tgbot import bot
from msg_handler import msg_handler
import asyncio


def main():
    handler = msg_handler(bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(handler.start_polling())
    loop.run_forever()


if __name__ == '__main__':
    main()

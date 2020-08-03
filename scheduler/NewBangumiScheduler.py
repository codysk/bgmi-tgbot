#!/usr/bin/python
# coding=utf-8

import os, json, asyncio, aiohttp, common, logging
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import channel_set, group_set
from tgbot import seng_message_to_err_channel, bot

prev_bangumi_key_list = []


async def check_update():
    logger = logging.getLogger(__name__)
    is_first = (len(prev_bangumi_key_list) == 0)
    # is_first = False    # For debug
    api_url = common.bgmi_api

    logger.info('checking update...')

    try:
        async with ClientSession() as client:
            content = await fetch(client, api_url)
    except asyncio.TimeoutError as _:
        logger.warning('fetch timeout!')
        await seng_message_to_err_channel(text='bgmi api fetch timeout!')
        return
    except (
        aiohttp.client_exceptions.ClientConnectionError,
        ConnectionError,
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionResetError
    ) as _:
        logger.warning('connect failed!')
        await seng_message_to_err_channel(text='bgmi api connect failed!')
        return

    updated_list = []
    new_bangumi_key_list = []
    api_data = json.loads(content)
    logger.debug(api_data)
    bangumi_list = api_data['data']
    for bangumi in bangumi_list:
        logger.debug(bangumi)
        bangumi_name = bangumi['bangumi_name']
        for episode in bangumi['player'].keys():
            bangumi_episode_key = '%s_episode_%s' % (bangumi_name, episode)
            new_bangumi_key_list.append(bangumi_episode_key)

            if bangumi_episode_key not in prev_bangumi_key_list:
                if not is_first:
                    updated_list.append('%s[%02d]' % (bangumi_name, int(episode)))
                pass
            pass

        pass

    logger.info(updated_list)
    # update prev list
    prev_bangumi_key_list.clear()
    prev_bangumi_key_list.extend(new_bangumi_key_list)

    if not len(updated_list) == 0:
        message = '有番组更新了~\n' \
                  '%s' % ('\n'.join(updated_list))

        # send to discuss
        for discuss_id in list(channel_set):
            logger.debug('send to channel: %s' %(channel_set))
            await bot.send_message(chat_id=discuss_id, text=message)

        # send to group
        for group_id in list(group_set):
            logger.debug('send to group: %s' % (group_id))
            await bot.send_message(chat_id=group_id, text=message)
        pass

    pass


async def fetch(client: ClientSession, url):
    async with client.get(url=url) as resp:
        assert resp.status == 200
        return await resp.text()


schedulers = AsyncIOScheduler()

# run for init
loop = asyncio.get_event_loop()
loop.run_until_complete(check_update())

schedulers.add_job(check_update, 'cron', second='0', minute='*/30')

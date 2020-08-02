#!/usr/bin/env python
# coding=utf-8

import os
import logging
import common
from aiogram import Bot

common.api_token = os.environ.get('api_token', False)
common.proxy_url = os.environ.get('proxy_url', '')
common.admin_userid = os.environ.get('admin_userid', '')
common.enable_public_command = os.environ.get('enable_public_command', 'Always')

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=common.api_token, proxy=common.proxy_url)

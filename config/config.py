#!/usr/bin/python3
# -*- coding: <utf-8> -*-

import os
import re
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

c5_csgo_url = 'https://www.c5game.com/csgo/default/result.html?min=%d&max=%d&sort=price.desc&page=%d'
c5_dota_url = 'https://www.c5game.com/dota.html?min=%d&max=%d&sort=price.desc&page=%d'
c5_csgo_item_url = 'https://www.c5game.com/csgo/default/result.html?k=%s'
c5_dota__item_url = 'https://www.c5game.com/dota.html?k=%s'
steam_market_listings = "https://steamcommunity.com/market/listings/%d/%s"

name_re = re.compile('<span class=" text-unique ">(.+?)</span>')
c5_price_re = re.compile('<span class="price">￥\s?(.+?)</span>')
page_re = re.compile('<li class="last"><a href=".+?;page=(\d+)"><span .+?</li>')
price_history_re = re.compile("var line1=(\[\[.+?]]);")
price_history_detail_re = re.compile("\[\"(.+?)\",(.+?),\"(\d+)\"]")

c5_re = [page_re, name_re, c5_price_re]
gameIds = {
    'dota': 570,
    'csgo': 730,
}
gameParams = {
    'dota': [c5_dota_url, c5_re],
    'csgo': [c5_csgo_url, c5_re],
}
gameLink = {
    'dota': c5_dota__item_url,
    'csgo': c5_csgo_item_url,
}

# 管理员邮箱地址
From = ''
# 管理员邮箱密码
pwd = ''
# 邮箱SMTP地址
smtp_server = ''
# 是否使用SSL
USE_SSL = False
# 邮箱端口
port = ''
# 收件人信息文件地址
ReceiverPath = os.path.join(base_dir, 'config/receivers')
# 结果保存地址
FileSavePath = os.path.join(base_dir, 'save/')

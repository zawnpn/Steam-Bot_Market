#!/usr/bin/python3
# -*- coding: <utf-8> -*-

from config.config import *
import requests
from lxml import etree
import time
import numpy as np
import pandas as pd
import json


def get_ex_rate():
    ex_url = 'http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=Code,Price'
    ex_html = requests.get(ex_url).content.decode('utf8')
    ex_rate_data = re.findall("{.*}", str(ex_html))[0]
    ex_rate = json.loads(ex_rate_data)
    return ex_rate["Data"][0][0][1]/10000


def get_price_ratio(_3rd_price, steam_price):
    ratio = float(_3rd_price)*1.15/(steam_price)
    return ratio


def get_market_detail(game_id, name, day_thresh=5):
    st_conn = requests.get(steam_market_listings % (game_id, name))
    content = st_conn.text
    st_conn.close()
    price_history_find = price_history_re.findall(content)
    if price_history_find:
        price_history = price_history_find[0]
        price_history_detail = price_history_detail_re.findall(price_history)
        if len(price_history_detail) >= day_thresh:
            prices = np.array([float(h[1]) for h in price_history_detail])[-day_thresh:]
            return [np.mean(prices), np.median(prices), np.ptp(prices), np.var(prices)]
        else:
            return None
    else:
        return None


def get_3rd_detail(_3rd_url, _3rd_re, p_min=5, p_max=500):
    page_conn = requests.get(_3rd_url % (p_min, p_max, 1))
    page_info = page_conn.text
    page_num = int(_3rd_re[0].findall(page_info)[0])
    page_conn.close()
    names = []
    prices = []
    for i in range(page_num):
        conn = requests.get(_3rd_url % (p_min, p_max, i + 1))
        content = conn.text
        conn.close()
        names.extend(_3rd_re[1].findall(content))
        prices.extend(_3rd_re[2].findall(content))
    return names, prices


def price_compare(game_name, _3rd_params, threshold=1, itemlen=0, sleeptime=2,
                  counts=5, p_min=5, p_max=500, outprint=True, savefile=True):
    _3rd_names, _3rd_prices = get_3rd_detail(_3rd_params[0], _3rd_params[1], p_min, p_max)
    ratios = []
    price_params = []
    item_names = []
    ex_rate = get_ex_rate()
    if itemlen <= 0:
        itemlen = len(_3rd_names)
    for i in range(itemlen):
        time.sleep(sleeptime)
        price_param = get_market_detail(gameIds[game_name], _3rd_names[i], day_thresh=counts)
        if price_param:
            ratio = get_price_ratio(_3rd_prices[i], price_param[1] * ex_rate)
            price_params.append(price_param)
            ratios.append(ratio)
            item_names.append(_3rd_names[i])
            if outprint and ratio < threshold:
                print("Name:%s|Ratio:%f|Avg:%f|Med:%f|Range:%f|Var:%f"
                      % (_3rd_names[i], ratio, price_param[0], price_param[1], price_param[2], price_param[3]))
        else:
            continue
    compare_result = np.column_stack((item_names, ratios, price_params))
    r_columns = ['Name', 'Ratio', 'Avg(%d)' % counts, 'Med(%d)' % counts, 'Range(%d)' % counts, 'Var(%d)' % counts]
    try:
        compare_result = pd.DataFrame(compare_result, columns=r_columns, dtype='object')

        compare_result[r_columns[1:]] = compare_result[r_columns[1:]].astype(float)
    except (ValueError, KeyError):
        return pd.DataFrame([])
    if savefile:
        if not os.path.exists(FileSavePath):
            os.makedirs(FileSavePath)
        compare_result.to_csv(FileSavePath + 'result_%s.csv' % game_name, index=False)
    return compare_result

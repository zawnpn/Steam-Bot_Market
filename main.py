#!/usr/bin/python3
# -*- coding: <utf-8> -*-

import argparse
from function.crawler import *
from function.mail import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get the best price!")
    parser.add_argument('--game', type=str, default='csgo', help='Choose a game')
    parser.add_argument('--sleep', type=int, default=2, help='Sleep time')
    parser.add_argument('--len', type=int, default=0, help='Amount of items')
    parser.add_argument('--range', type=float, nargs=2, default=[5.0, 500.0], help='Price range')
    parser.add_argument('--thresh', type=float, default=1, help='Threshold of ratio')
    parser.add_argument('--days', type=int, default=5, help='Count days')
    parser.add_argument('--save', '-s', action='store_true', default=False, help='Save an output file')
    parser.add_argument('--print', '-p', action='store_true', default=False, help='Instant output')
    parser.add_argument('--mail', '-m', action='store_true', default=False, help='Send result by mail')
    args = parser.parse_args()

    gameParam = gameParams[args.game]
    final_result = price_compare(args.game, gameParam, sleeptime=args.sleep, itemlen=args.len, threshold=args.thresh,
                                 days=args.days, savefile=args.save, outprint=args.print)
    if args.mail:
        if not final_result.empty:
            good_result = final_result[final_result['Ratio'] < args.thresh]
            if not good_result.empty:
                send_mail(good_result, args.game, USE_SSL)

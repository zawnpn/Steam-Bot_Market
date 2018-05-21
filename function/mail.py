#!/usr/bin/python3
# -*- coding: <utf-8> -*-

from config.config import *
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
import smtplib
import time
from traceback import format_tb
import sys
sys.path.append("..")


# 编码发件人信息
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 登录邮件
def login(use_ssl):
    if use_ssl:
        server = smtplib.SMTP_SSL(smtp_server, port)
    else:
        server = smtplib.SMTP(smtp_server, port)
    server.set_debuglevel(1)
    server.login(From, pwd)
    return server


# 发送邮件
def send(receiver, message, server, game_name):
    from_addr = From
    to_addr = receiver
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'html', 'utf-8'))
    msg['Subject'] = Header('[%s]Good Ratio!' % game_name.upper(), 'utf-8').encode()
    msg['From'] = _format_addr('Steam-Bot<%s>' % from_addr)
    msg['To'] = _format_addr('Receiver<%s>' % to_addr)
    att = MIMEText(open(FileSavePath + 'result_%s.csv' % game_name, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'test/csv'
    att["Content-Disposition"] = 'attachment; filename="result_%s.csv"' % game_name
    msg.attach(att)
    server.sendmail(from_addr, [to_addr], msg.as_string())


# 发送多个邮件
def sends(receivers, message, game_name, use_ssl):
    server = login(use_ssl)
    for receiver in receivers:
        print("send to %s" % receiver)
        try:
            send(receiver, message, server, game_name)
        except Exception as exc:
            print(format_tb(exc.__traceback__)[0])
        time.sleep(8)
    server.quit()


# 构造邮件发送信息
def make_message(game_details, game_name):
    message = """
    <div style="font-size: 14px; padding: 0px; height: auto;min-height: auto; 
    font-family:"lucida Grande&quot", Verdana; position: relative; zoom: 1; margin-right: 0px;">
    """
    for i in range(game_details.shape[0]):
        game = game_details.iloc[i]
        message += """
        <div style="background-color:white;border:1px solid #C8C8C8;
        box-shadow:0 0 5px rgba(0,0,0,0.25);margin:20px 0 40px;width:500px;">
        <div style="font-size: 14px; padding: 0pt; height: auto; font-family: 'lucida Grande',Verdana; 
        margin:20px">
        <h2 style="font-size:18px;font-weight:bold;margin:10px 0;word-wrap: break-word;
        word-break: break-all">%s</h2>
        """ % game[0]
        message += """
        <p style="margin:0; "><span style="color:#b2b2b2">Ratio:</span>%f</p>
        <p style="margin:0; "><span style="color:#b2b2b2">Avg:</span>$%f</p>
        <p style="margin:0; "><span style="color:#b2b2b2">Med:</span>$%f</p>
        <p style="margin:0; "><span style="color:#b2b2b2">Range:</span>$%f</p>
        <p style="margin:0; "><span style="color:#b2b2b2">Var:</span>%f</p>
        </div>
        """ % (game[1], game[2], game[3], game[4], game[5])
        message += """
        <div style="background-color: rgb(241, 241, 241); padding: 10px; display: block;">
        <a style="background-color: #DBDBDB;border: none;color: black;padding: 3px 10px;
        text-align: center;text-decoration: none;display: inline-block;" href="%s">View Detail</a>
        </div></div>
        """ % gameLink[game_name] % game[0].replace(' ', '%20')
    message += """
    <p style="font-size: 10px;color:#b2b2b2">To unsubscribe, please contact zwp@oncemath.com
    <br />Powered by <a href="http://www.oncemath.com">ONCE.MATH</a></p>
    </div>
    """
    return message


# 发送邮件
def send_mail(game_details, game_name, use_ssl=False):
    message = make_message(game_details, game_name)
    with open(ReceiverPath, 'r') as f:
        receivers = f.readlines()
        receivers = [receivers[2*i+1][:-1] for i in range(int(len(receivers)/2))]
        print(receivers)
    sends(receivers, message, game_name, use_ssl)

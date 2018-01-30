#!/usr/bin/env python3

import os
import sys
import argparse
from slackclient import SlackClient

SLACK_BOT_TOKEN = ""
MAX_LEN = 50

def shift(msg, offset, delimiters):
    length = len(msg)
    l = []
    l.append(delimiters)
    if (length - offset) > 0:
        l.append('{}'.format(''))
        l.append(msg[(length - offset):MAX_LEN - (offset % MAX_LEN)])
    else:
        l.append('{}'.format(' ' * (offset - length) ))
        l.append(msg[:MAX_LEN - (offset % MAX_LEN)])
    l.append('{}'.format(' ' * (MAX_LEN - len(l[1]) - len(l[2]) - length) ))
    l.append(delimiters)
    return "".join(l)

def main(msg, channel, repeat, delimiters):
    sc = SlackClient(SLACK_BOT_TOKEN)

    offset = 0
    response = sc.api_call("chat.postMessage", channel=channel, text=shift(msg, offset, delimiters))
    channel = response['channel']
    ts = response['ts']

    for _ in range(int(repeat)):
        for offset in range(MAX_LEN):
            response = sc.api_call("chat.update", ts=ts, channel=channel, text=shift(msg, offset, delimiters))
            channel = response['channel']
            ts = response['ts']
    response = sc.api_call("chat.update", ts=ts, channel=channel, text="{}{}{}".format(delimiters, msg, delimiters))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--channel', '-c', action='store', default=None)
    parser.add_argument('--message', '-m', action='store', default=None)
    parser.add_argument('--repeat', '-r', action='store', default=2)
    parser.add_argument('--delimiters', '-d', action='store', default='|')
    args = parser.parse_args()
    msg = args.message

    with open("SLACK_BOT_TOKEN", 'r+') as f:
        SLACK_BOT_TOKEN = f.readline()
    if SLACK_BOT_TOKEN == "":
        print("SLACK_BOT_TOKEN not read or set")
        sys.exit(0)
    if len(msg) > MAX_LEN:
        print("Sorry message too long")
        sys.exit(0)

    main(msg, args.channel, args.repeat, args.delimiters)
    sys.exit(1)

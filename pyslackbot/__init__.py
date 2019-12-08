import sys
import six
import os
import json


def is_allowed_python_version():
    if six.PY2:
        return sys.version_info >= (2, 7)
    elif six.PY3:
        return sys.version_info >= (3, 6)
    return False


if not is_allowed_python_version():
    print("Error: 'Python2.7+' or 'Python 3.6+' required")
    sys.exit(1)

from pyslackbot.slackbot import SlackBot

slack_api_token = os.environ.get('SLACK_API_TOKEN', '').strip()
if not slack_api_token:
    print("Error: os environment variable 'SLACK_API_TOKEN' required")
    sys.exit(1)

sb = SlackBot(token=slack_api_token)

@sb.handler
def handle_horde(msg):
    if '호드' in msg.text:
        msg.react(':crossed_swords:')
        # msg.reply(':crossed_swords: 호드를 위하여!')
        # msg.channel.say(':crossed_swords: 호드를 위하여!')
        # TODO: ask 기능 만들기
        # msg.channel.ask('진영을 선택하세요.', {'호드': 1, '얼라': 2}, use_button=True)
        return True


@sb.handler
def handle_echo(msg):
    # print('Received:', json.dumps(payload['data'], indent=2, ensure_ascii=False))
    #sb.say(msg.channel.id, msg.text)
    #return 'ok!'
    return msg.text


def main():
    return sb.runforever()


if __name__ == '__main__':
    sys.exit(main())

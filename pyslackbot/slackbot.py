# from __future__ import print_function
import six
import os
import sys
import copy
import json
import time
import inspect
from datetime import datetime
from collections import OrderedDict
from functools import wraps
from memorize import memorize


class SlackMemberProfile:
    def __init__(self, **kw):
        self._data = kw

    def todict(self):
        return copy.copy(self._data)

    @property
    def title(self):
        return self._data.get('title', '')

    @property
    def phone(self):
        return self._data.get('phone', '')

    @property
    def skype(self):
        return self._data.get('skype', '')

    @property
    def real_name(self):
        return self._data.get('real_name', '')

    @property
    def real_name_normalized(self):
        return self._data.get('real_name_normalized', '')

    @property
    def display_name(self):
        return self._data.get('display_name', '')

    @property
    def display_name_normalized(self):
        return self._data.get('display_name_normalized', '')

    @property
    def status_text(self):
        return self._data.get('status_text', '')

    @property
    def status_emoji(self):
        return self._data.get('status_emoji', '')

    @property
    def status_expiration(self):
        return self._data.get('status_expiration', 0)

    @property
    def avatar_hash(self):
        return self._data.get('avatar_hash', '')

    @property
    def email(self):
        return self._data.get('email', '')

    @property
    def first_name(self):
        return self._data.get('first_name', '')

    @property
    def last_name(self):
        return self._data.get('last_name', '')

    @property
    def image_24(self):
        return self._data.get('image_24', '')

    @property
    def image_32(self):
        return self._data.get('image_32', '')

    @property
    def image_48(self):
        return self._data.get('image_48', '')

    @property
    def image_72(self):
        return self._data.get('image_72', '')

    @property
    def image_192(self):
        return self._data.get('image_192', '')

    @property
    def image_512(self):
        return self._data.get('image_512', '')

    @property
    def status_text_canonical(self):
        return self._data.get('status_text_canonical', '')

    @property
    def team(self):
        return self._data.get('team')

    @property
    def bot_id(self):
        return self._data.get('bot_id', '')

    @property
    def api_app_id(self):
        return self._data.get('api_app_id', '')

    @property
    def always_active(self):
        return self._data.get('always_active', False)


class SlackMember:
    def __init__(self, **kw):
        self._data = kw

    def todict(self):
        return copy.copy(self._data)

    def say(self, text):
        raise NotImplementedError('todo: implement say(direct message)')

    @property
    def id(self):
        return self._data.get('id')

    @property
    def team_id(self):
        return self._data.get('team_id')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def deleted(self):
        return self._data.get('deleted', True)

    @property
    def color(self):
        return self._data.get('color', '000000')

    @property
    def real_name(self):
        return self._data.get('real_name')

    @property
    def tz(self):
        return self._data.get('tz', None)

    @property
    def tz_label(self):
        return self._data.get('tz_label')

    @property
    def tz_offset(self):
        return self._data.get('tz_offset')

    @property
    def profile(self):
        return SlackMemberProfile(**self._data.get('profile', {}))

    @property
    def is_admin(self):
        return self._data.get('is_admin', False)

    @property
    def is_owner(self):
        return self._data.get('is_owner', False)

    @property
    def is_primary_owner(self):
        return self._data.get('is_primary_owner', False)

    @property
    def is_restricted(self):
        return self._data.get('is_restricted', False)

    @property
    def is_ultra_restricted(self):
        return self._data.get('is_ultra_restricted', False)

    @property
    def is_bot(self):
        return self._data.get('is_bot', False)

    @property
    def is_app_user(self):
        return self._data.get('is_app_user', False)

    @property
    def updated(self):
        return self._data.get('updated', 0)


class SlackMemberJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (SlackMember, SlackMemberProfile)):
            return o.todict()
        return o.__dict__


class SlackMessage:
    def __init__(self, payload):
        self._data = payload

    @property
    def web_client(self):
        return self._data['web_client']

    def todict(self):
        return copy.copy(self._data)

    def reply(self, text):
        return self.channel.say(text, thread_ts=self._data['data']['ts'])

    def react(self, emoji):
        if emoji.startswith(':'):
            emoji = emoji[1:]
        if emoji.endswith(':'):
            emoji = emoji[0:-1]
        _sc = SlackClient()
        return self.web_client.reactions_add(channel=self.channel.id, name=emoji, timestamp=self._data['data']['ts'])

    @property
    def ts(self):
        # TODO: time zone
        return datetime.fromtimestamp(self._data['data']['ts'])

    @property
    def client_msg_id(self):
        return self._data['data']['client_msg_id']

    @property
    def text(self):
        return self._data['data']['text']

    @property
    def user(self):
        _sc = SlackClient()
        return _sc._members.get(self._data['data']['user'])

    @property
    def channel(self):
        _sc = SlackClient()
        return _sc._channels.get(self._data['data']['channel'])


class SlackChannel:
    def __init__(self, members, **kw):
        self._data = kw

    def todict(self):
        return copy.copy(self._data)

    def say(self, text, thread_ts=None):
        _sc = SlackClient()
        return _sc.say(channel=self.id, text=text, thread_ts=thread_ts)

    @property
    def id(self):
        return self._data.get('id')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def created(self):
        return datetime.fromtimestamp(self._data.get('created', 0))

    @property
    def creator(self):
        _sc = SlackClient()
        return _sc._members.get(self._data.get('creator'))

    @property
    def is_archived(self):
        return self._data.get('is_archived')

    @property
    def is_general(self):
        return self._data.get('is_general')

    @property
    def name_normalized(self):
        return self._data.get('name_normalized')

    @property
    def is_shared(self):
        return self._data.get('is_shared')

    @property
    def is_private(self):
        return self._data.get('is_private')

    @property
    def members(self):
        _sc = SlackClient()
        return tuple([_sc._members.get(_id) for _id in self._data.get('members', [])])

    @property
    def topic(self):
        return self._data.get('topic', {})

    @property
    def purpose(self):
        return self._data.get('purpose', {})

    @property
    def num_members(self):
        return self._data.get('num_members', 0)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SlackBotError(Exception):
    pass


class SlackBot:
    def __init__(self, token=None, slack_client=None):
        if token is None:
            token = os.environ.get('SLACK_API_TOKEN')

        if not token:
            raise SlackBotError("os environment 'SLACK_API_TOKEN' required")

        self.token = token

        import ssl
        from slack import WebClient
        # ssl_context = ssl.SSLContext()
        # self.sc = WebClient(token=token, ssl=ssl_context)
        self.handlers = []
        # self._channels = {_x.id: _x for _x in self.get_channels()}  # {channel_id: SlackChannel(...), ...}
        # self._members = {_x.id: _x for _x in self.get_members()}    # {user_id: SlackMember(...), ...}

    def add_hander(self, func):
        self.handlers.append(func)

    def handler(self, func):
        self.add_hander(func)
        @wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        return wrapper

    @memorize(timeout=60)
    def get_members(self):
        #print('get_members called')
        self._members = {_x['id']: SlackMember(**_x) for _x in self.sc.api_call('users.list').get('members', [])}
        return tuple(self._members.values())

    @memorize(timeout=60)
    def get_channels(self):
        self._channels = {_x['id']: SlackChannel(**_x) for _x in self.sc.api_call('channels.list').get('channels', [])}
        return tuple(self._channels.values())

    def say(self, channel, text, thread_ts=None):
        try:
            resp = self.sc.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts)
            return resp['ok']
        except:
            pass
        return False

    def runforever(self):
        from slack import RTMClient
        @RTMClient.run_on(event='message')
        def handle_message(**payload):
            if 'bot_id' in payload['data']:
                return
            message = SlackMessage(payload)
            for func in self.handlers:
                resp_text = func(message)
                if resp_text:
                    if isinstance(resp_text, str):
                        self.say(message.channel.id, resp_text)
                    break

        rtm_client = RTMClient(token=self.token)
        rtm_client.start()

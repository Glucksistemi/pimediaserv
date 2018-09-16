import json
import re

SIMPLE_COMMANDS = [
    'pause',
    'sub_select',
    'switch_audio',
    'mute',
    'vo_fullscreen',
    'quit'
]

VALUED_COMMANDS = [
    'volume',
    'loop',
    'seek',

]
PROPERTIES = [
    'volume',
    'path',
    'filename',
    'length',
    'percent_pos',
    'time_pos',
    'pause'
]


class Command():
    command = ''
    need_answer = False
    args = []

    def __init__(self, args, command=''):
        print(command)
        self.args = args
        if command and not self.command:
            self.command = command

    def form_command(self):
        return self.command

    def parse_resp(self, resp):
        return resp

    def send(self, tcp_func):
        return self.parse_resp(json.loads(tcp_func(self.form_command(),self.need_answer)))


class ValuedCommand(Command):
    def form_command(self):
        return ' '.join([self.command, self.args.get('value',''), self.args.get('abs','')])


class PropertyHandler(Command):
    need_answer = True

    def form_command(self):
        if self.args.get('property','') not in PROPERTIES:
            return ''
        if self.args.get('mode','get') == 'get':
            return 'pausing_keep_force get_property '+self.args.get('property','')
        elif self.args.get('mode','get') == 'set':
            return 'pausing_keep_force set_property '+self.args.get('property','')+' '+self.args.get('value','')
        return ''

    def parse_resp(self, resp):
        if self.args.get('mode','') == 'get':
            print('response:', resp, 'prop:', self.args.get('property',''))
            rg = re.compile(r'^ANS_(?P<property>.+)=(?P<value>.+)$')
            try:
                return rg.match(resp[0]).groupdict()
            except IndexError:
                return {"property": self.args.get('property',None), "value": None}
        else:
            return {}


def get_command_object(command, args):
    if command in SIMPLE_COMMANDS:
        return Command(args, command)
    if command in VALUED_COMMANDS:
        return ValuedCommand(args,command)
    if command == 'property':
        return PropertyHandler(args)
    else:
        return {'error': 'wrong command'}


def get_property(property, tcp):
    return PropertyHandler({'mode': 'get', 'property': property}).send(tcp).get('value','')


def set_property(property, value, tcp):
    return PropertyHandler(args={'mode': 'set', 'property': property, 'value': value, 'abs': ''}, command='').send(tcp)
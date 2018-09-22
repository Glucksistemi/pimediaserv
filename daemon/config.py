import json
import sys
# mplayer settings
MPLAYER_COMMAND_STRING = "mplayer {0} -slave -quiet 2>/dev/null"

# TCP settings
TCP_PORT = 9805
TCP_HOST = 'localhost' # for testing client

# common setting
FREQENCY = 0.01 # main loop sleep time for every iteration


class Config(): # TODO: make basic class for config handling and inherit for daemon and flaskapp
    tcp_port = 9800
    tcp_host = 'localhost'
    frequency = 0.01
    mplayer_command_string = "mplayer {0} -slave -quiet 2>/dev/null"

    def __init__(self, given_path=None):
        if given_path:
            path = given_path
        else:
            try:
                path = sys.argv[1]
            except IndexError:
                path = '../config.json' # default path
        try:
            with open(path) as cfile:
                config = json.loads(cfile.read())
        except FileNotFoundError:
            return
        try:
            self.tcp_port = config['tcp']['port']
            self.tcp_host = config['tcp']['host']
            self.frequency = config['daemon']['frequency']
            self.mplayer_command_string = config['daemon']['mplayer_command_string']
        except KeyError:
            print('wrong_configuration! Using defaults')

import json
import time
from re import escape

from socketserver import SocketHandler
from mplayer import MPlayerManager
from config import Config

config = Config()
#starting TCP server
socket_handler = SocketHandler(config.tcp_port)

# creating MplayerManager instance
mplayer = MPlayerManager()


def command_compare(command, waitfor):
    return command[2:len(waitfor)+2] == waitfor

# starting mainloop
try:
    break_condition = 0
    while not break_condition:
        time.sleep(config.frequency)
        command = socket_handler.get_data_from_socket()
        if command:
            if command_compare(command, '_open'):
                if mplayer.is_active:
                    mplayer.kill()
                current_data = mplayer.run(config.mplayer_command_string.format(escape(command[8:])))
                socket_handler.send_response(json.dumps(current_data))
            elif command_compare(command, '_status'):
                if not mplayer.is_active:
                    socket_handler.send_response(json.dumps({'mplayer_on': False}))
                else:
                    socket_handler.send_response(json.dumps({'mplayer_on': True}))
            elif command_compare(command, '_killd'):
                if mplayer.is_active:
                    mplayer.kill()
                socket_handler.send_response(json.dumps({'exiting': True}))
                socket_handler.close()
                break_condition = 1
            elif command_compare(command, '_reconf'):
                config = Config(escape(command[10:]))
                socket_handler.close()
                socket_handler = SocketHandler(config.tcp_port)
            else:
                if mplayer.is_active:
                    rsp = mplayer.send_command(command[2:], int(command[0]))
                else:
                    rsp = {'error': True, 'error_message': 'MPlayer not running'}
                socket_handler.send_response(
                    json.dumps(rsp)
                )
except KeyboardInterrupt:
    print('keyboard interrupt caught')
    socket_handler.close()
    exit(2)
except:
    print('other error caught. quiting...')
    socket_handler.close()
    raise

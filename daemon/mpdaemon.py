import json
import time
import re
from socketserver import SocketHandler
from re import escape

from mplayer import MPlayerManager

import config

#starting TCP server
socket_handler = SocketHandler(config.TCP_PORT)

# creating MplayerManager instance
mplayer = MPlayerManager()


def command_compare(command, waitfor):
    return command[2:len(waitfor)+2] == waitfor

# starting mainloop
try:
    break_condition = 0
    while not break_condition:
        time.sleep(config.FREQENCY)
        command = socket_handler.get_data_from_socket()
        if command:
            if command_compare(command, '_open '):
                if mplayer.is_active:
                    mplayer.kill()
                current_data = mplayer.run(config.MPLAYER_COMMAND_STRING.format(escape(command[8:])))
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
            else:
                if mplayer.is_active:
                    rsp = mplayer.send_command(command[2:], int(command[0]))
                else:
                    rsp = {'error': True, 'error_message': 'MPlayer not running'}
                socket_handler.send_response(
                    json.dumps(rsp)
                )
except KeyboardInterrupt:
    socket_handler.close()
    raise

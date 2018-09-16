from flask import Flask, request
import json
import fsselector
from tcpclient import send_request
from decorators import json_response
from config import TCP_PORT, TCP_HOST, ALLOW_CORS, ALLOW_DAEMON_KILL
from flask_cors import CORS
import re
from commands import get_command_object, PropertyHandler, get_property
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
if ALLOW_CORS:
    CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

def error(error_data):
    return {'error': True, 'error_data': error_data}


def tcp(request, need_answer = False):
    return send_request(TCP_HOST, TCP_PORT, request, need_answer)


@app.route('/', methods=['GET'])
def index():
    return 'hello, '+request.args.get('name','')+'!'


@app.route('/navigate')
@json_response
def navigate():
    if not request.args.get('root',''):
        return fsselector.get_roots()
    else:
        return fsselector.get_folder_contents(
            int(request.args.get('root',-1)),
            request.args.get('path','')
        )


@app.route('/play',methods=['GET'])
@json_response
def play():
    if request.args.get('root','ooops') != 'ooops' and request.args.get('content',''):
        path = fsselector.get_full_path(request.args.get('root',''), request.args.get('content',''))
        if path:
            tcp('_open '+path)
            filename = PropertyHandler(args={'property': 'filename', 'mode': 'get'}).send(tcp)
            tcp('vo_fullscreen')
            return {'error': False, 'filename': filename}

        else:
            return {'error': True, 'error_data': 'file not found'}
    return {'error': True, 'error_data': 'not enough arguments'}


@app.route('/control')
@json_response
def control():
    command = request.args.get('command','')
    if command:
        return get_command_object(args=request.args, command=command).send(tcp)


@app.route('/props')
@json_response
def props():
    return PropertyHandler(args=request.args, command='property').send(tcp)


@app.route('/status')
@json_response
def status():
    st = {}
    try:
        st['mplayer_on'] = json.loads(tcp('_status', True)).get('mplayer_on',False)
    except ConnectionRefusedError:
        return {'error': 'true', 'error_data': 'connection refused'}
    if not st['mplayer_on']:
        return st
    st['volume'] = get_property('volume', tcp)
    st['position'] = {
        'percent': get_property('percent_pos', tcp),
        'seconds': get_property('time_pos', tcp)
    }
    st['filename'] = get_property('filename', tcp)
    st['paused'] = get_property('pause', tcp)
    return st


@app.route('/stop')
@json_response
def quit():
    return  get_command_object(args=request.args, command='quit').send(tcp)


@app.route('/killd')
@json_response
def kill_daemon():
    if not ALLOW_DAEMON_KILL:
        return {'error': True, 'error_data': 'daemon killing is not allowed'}
    return json.loads(tcp('_killd',True))
CONTENT_PATHS = [
    {
        "name": "Видео",
        "path": "/home/gluck/Видео"
    },
    {
        "name": "Музыка",
        "path": "/home/gluck/Музыка"
    }
]
TCP_HOST = 'localhost'
TCP_PORT = 9805
ALLOW_CORS = True
ALLOW_DAEMON_KILL = True

class Config(): # TODO: make basic class for config handling and inherit for daemon and flaskapp
    tcp_port = 9800
    tcp_host = 'localhost'
    allow_cors = False
    allow_daemon_kill = False
    content_paths = []
    allowed_commands = {'simple_commands': [], 'valued_commands': [], 'properties': []}

    def __init__(self, given_path='../config.json'):
        if given_path:
            path = given_path
        else:
            try:
                path = sys.argv[1]
            except IndexError:
                path = '../config.json' # default path
        try:
            with open(src) as cfile:
                config = json.loads(cfile.read())
        except FileNotFoundError:
            return
        try:
            self.tcp_port = config['tcp']['port']
            self.tcp_host = config['tcp']['host']
            self.allow_cors = config['application']['allow_cors']
            self.allow_daemon_kill = config['application']['allow_daemon_kill']
            self.content_paths = config['content_paths']
            self.allowed_commands = config['allowed_commands']

        except KeyError:
            print('wrong_configuration! Using defaults')

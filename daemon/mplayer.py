import subprocess
import shlex
from threading import Thread
from time import sleep


class MPlayerManager(object):
    is_active = False
    mplayer = None
    thread = None
    statedict = {
        'await': False,
        'output': []
    }

    def get_output(self, out, statedict):
        for line in iter(out.readline, b''):
            self.is_active = True
            if statedict['await']:
                statedict['output'].append(line)
            if line == '':
                break
        self.is_active = False
        out.close()

    def run(self, command):
        print(1)
        self.is_active = True
        self.statedict = {
            'await': True,
            'output': []
        }
        print(command)
        self.mplayer = subprocess.Popen(
            shlex.split(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        self.thread = Thread(target=self.get_output, args=(self.mplayer.stdout, self.statedict))
        self.thread.daemon = True
        self.thread.start()
        sleep(2)
        self.statedict['await'] = False
        return self.statedict['output']

    def write(self, command):
        self.mplayer.stdin.write(command + '\n')
        self.mplayer.stdin.flush()

    def send_command(self, command, need_return = False):
        print(self.statedict)
        if need_return:
            self.statedict['output'].clear()
            self.statedict['await'] = True
            self.write(command)
            sleep(0.05)
            return self.statedict['output'].copy()
        self.write(command)
        return []

    def kill(self):
        self.mplayer.kill()
        self.mplayer = None



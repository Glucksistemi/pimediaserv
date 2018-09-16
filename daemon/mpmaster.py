import subprocess, time, shlex, select, sys
from threading import Thread

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out):
    for line in iter(out.readline, b''):
        lines.append(line)
        if line == '':
            break
    out.close()
    print('stopped')
lines = []
MPLAYER_CALL_STRING = 'mplayer /home/gluck/Klass.2007.720p.mkv -slave -quiet'
mplayer = subprocess.Popen(shlex.split(MPLAYER_CALL_STRING), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True, bufsize=1, close_fds=ON_POSIX)
t = Thread(target=enqueue_output, args=(mplayer.stdout,))
t.daemon = True # thread dies with the program
t.start()
line = ''
time.sleep(1)
print('\n'.join(lines))
lines = []
for x in range(0,5):
    time.sleep(1)
    #mplayer.stdin.write('seek 5850 2\n')
    #mplayer.stdin.flush()
    print(x)
mplayer.kill()
time.sleep(1)
print(mplayer)
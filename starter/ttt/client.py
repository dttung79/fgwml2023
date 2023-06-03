import getopt, sys
from ttt_client import TicTacToeClient

arguments = sys.argv[1:]

shortOptions = 'h:p:m:ivn:'
longOptions = ['host', 'port', 'interact', 'verbose', 'name', 'move']

try:
    arguments, values = getopt.getopt(arguments, shortOptions, longOptions)
except getopt.error as err:
    print (str(err))
    sys.exit(2)

interact = False
verbose = False

for arg, val in arguments:
    if arg in ('-h', '--host'):
        host = val
    elif arg in ('-p', '--port'):
        port = val
    elif arg in ('-i', '--interact'):
        interact = True
    elif arg in ('-v', '--verbose'):
        verbose = True
    elif arg in ('-n', '--name'):
        name = val
    elif arg in ('-m', '--move'):
        move = val

port = int(port)
print('Host:', host, 'Port:', port, 'Interact:', interact, 'Name:', name, 'Move', move)
client = TicTacToeClient(name, move, host, port, interact, verbose)
client.start()

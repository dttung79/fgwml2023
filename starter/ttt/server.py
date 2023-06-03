import getopt, sys
from ttt_server import TicTacToeServer

arguments = sys.argv[1:]

shortOptions = 'h:p:iv'
longOptions = ['host', 'port', 'interact', 'verbose']

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

print('Host:', host, 'Port:', port, 'Interact:', interact)
port = int(port)
server = TicTacToeServer(host, port, interact, verbose)
server.start()

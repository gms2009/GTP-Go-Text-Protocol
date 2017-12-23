import sys
import re
import random

#an engine is expected to keep track of the following state information
boardsize = 19
komi = 6.5
protocol_version = 2
name = 'Go Away'
version = '1.0'
commands = ['protocol_version',                     #supported commands
            'name',
            'version',
            'known_command',
            'list_commands',
            'quit',
            'boardsize',
            'clear_board',
            'komi',
            'play',
            'genmove']

def quit():                                         #function for the engine to close the connection
    sys.stdout.write('engine closed\n')

def clear_board():                                  #funtion for clearing the board
    sys.stdout.write('board has been cleared\n')

def resign():                                       #function for resigning operation
    sys.stdout.write('one player resigns the game\n')

def play(color, coord):
    #here should be code for adding the stone to board

    sys.stdout.write(color + ' play at ' + str(coord) + '\n')

def genmove(color):
    num = random.randint(0, boardsize * boardsize + 1)
    #here should be code for determing where the next stone is to be put

    if num == 0:
        return 'resign'
    else:
        return color + ' ' + num_to_coor(num)

def num_to_coor(num):
    if num == boardsize * boardsize + 1:
        return 'pass'
    row = num // boardsize
    col = num % boardsize
    return chr(col + 96) + str(boardsize - row)

def color_parser(arguments):
    if len(arguments) == 1:
        color = arguments[0].lower()
        if color in ['w', 'white']:
            return 'w'
        elif color in ['b', 'black']:
            return 'b'

def move_parser(arguments):
    if len(arguments) == 2:
        color = arguments[0].lower()
        vertex = arguments[1].lower()

        if color in ['w', 'white']:
            color = 'w'
        elif color in ['b', 'black']:
            color = 'b'
        else:
            return None

        if vertex == 'pass':
            return  [color, 362]

        col = ord(vertex[0]) - 96
        if vertex[1:].isdigit():
            row = int(vertex[1:])
            print(row, col, boardsize)
            if col >= 1 and col <= boardsize and row >= 1 and row <= boardsize:
                return [color, (boardsize - row) * boardsize + col]

def gtp_parser():
    global boardsize
    while True:
        id = ''
        raw_input = sys.stdin.readline().strip(' \n')
        if '#' in raw_input:
            raw_input = raw_input[:raw_input.find('#')]
        cmd = raw_input.split(' ')
        if cmd[0].isdigit():
            id = cmd[0]
            command_name = cmd[1]
            arguments = cmd[2:]
        else:
            command_name = cmd[0]
            arguments = cmd[1:]
        # sys.stdout.write(id + command_name + str(arguments))
        if command_name == 'play':
            if arguments == ['resign']:
                resign()
                sys.stdout.write('=' + id + ' \n\n')
            else:
                move = move_parser(arguments)
                if move:
                    play(move[0], move[1])
                    sys.stdout.write('=' + id + ' \n\n')
                else:
                    sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'genmove':
            color = color_parser(arguments)
            if color:
                reply = genmove(color)
                sys.stdout.write('=' + id + ' ' + reply + '\n\n')
                if reply == 'resign':
                    break
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'protocol_version':
            if arguments == []:
                sys.stdout.write('=' + id + ' ' + str(protocol_version) + '\n\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'name':
            if arguments == []:
                sys.stdout.write('=' + id + ' ' + str(name) + '\n\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'version':
            if arguments == []:
                sys.stdout.write('=' + id + ' ' + str(version) + '\n\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'known_command':
            if len(arguments) == 1:
                if arguments[0] in commands:
                    sys.stdout.write('=' + id + ' true\n\n')
                else:
                    sys.stdout.write('=' + id + ' false\n\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'list_commands':
            if arguments == []:
                sys.stdout.write('=' + id + ' ')
                for command in commands:
                    sys.stdout.write(command + '\n')
                sys.stdout.write('\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'quit':
            if arguments == []:
                quit()
                sys.stdout.write('=' + id + ' \n\n')
                break
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'boardsize':
            if len(arguments) == 1 and arguments[0].isdigit():
                size = int(arguments[0])
                if size >= 2 and size <= 25:
                    boardsize = size
                    sys.stdout.write('=' + id + ' \n\n')
                else:
                    sys.stdout.write('?' + id + ' unacceptable size\n\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'clear_board':
            if arguments == []:
                clear_board()
                sys.stdout.write('=' + id + ' \n\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        elif command_name == 'komi':
            value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
            if len(arguments) == 1 and value.match(arguments[0]):
                komi = float(arguments[0])
                sys.stdout.write('=' + id + ' \n\n')
            else:
                sys.stdout.write('?' + id + ' invalid command format\n\n')
        else:
            sys.stdout.write('?' + id + ' unknown command\n\n')

gtp_parser()

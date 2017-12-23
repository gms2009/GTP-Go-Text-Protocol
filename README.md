# GTP-Go-Text-Protocol
This a simple implementation of GTP for Go engines in Python 3.
Support commands(11):

`protocol_version`

`name``version`

`known_command`

`list_commands`

`quit``boardsize`

`clear_board``komi`

`play``genmove`
1. An engine is expected to keep track of the following state information(with default value)

`boardsize = 19`

`komi = 6.5`

`protocol_version = 2`

`name = 'Go Away`

`version = '1.0'`
2. Function genmove(color) requires code for determing where the next stone is to be put
3. Function play(color, coord)/clear_board() requires engine to update the board state.
4. Function quit()/resign() is related to end the game.
5. For the detailed input output format, please refer to Section 6 in [Specification of the Go Text Protocol, version 2,
draft 2](http://www.lysator.liu.se/~gunnar/gtp/gtp2-spec-draft2.pdf)

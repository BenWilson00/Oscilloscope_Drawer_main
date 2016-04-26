import pygame
from basic import *

cursors = {
'arrow' : (               #24x24
	'#                       ',
	'##                      ',
	'#.#                     ',
	'#..#                    ',
	'#...#                   ',
	'#....#                  ',
	'#.....#                 ',
	'#......#                ',
	'#.......#               ',
	'#........#              ',
	'#.........#             ',
	'#..........#            ',
	'#......#####            ',
	'#...#..#                ',
	'#..# #..#               ',
	'#.#  #..#               ',
	'##    #..#              ',
	'      #..#              ',
	'       ##               ',
	'                        ',
	'                        ',
	'                        ',
	'                        ',
	'                        '),

'click' : (               #24x24
	'     @#                 ',
	'    #..#                ',
	'    #..#                ',
	'    #..#                ',
	'    #..#                ',
	'    #..###              ',
	'    #..#..###           ',
	'    #..#..#..##         ',
	'    #..#..#..#.#        ',
	'### #..#..#..#..#       ',
	'#..##........#..#       ',
	'#...#...........#       ',
	' #..............#       ',
	'  #.............#       ',
	'  #.............#       ',
	'   #............#       ',
	'   #...........#        ',
	'    #..........#        ',
	'    #..........#        ',
	'     #........#         ',
	'     #........#         ',
	'     ##########         ',
	'                        ',
	'                        '),

'grab' : (               #24x24
	'        @#              ',
	'     ###..###           ',
	'    #..#..#..##         ',
	'    #..#..#..#.#        ',
	'  ###..#..#..#..#       ',
	' #..#........#..#       ',
	' #..#...........#       ',
	' #..............#       ',
	'  #.............#       ',
	'  #.............#       ',
	'   #............#       ',
	'   #...........#        ',
	'    #..........#        ',
	'    #..........#        ',
	'     #........#         ',
	'     #........#         ',
	'     ##########         ',
	'                        ',
	'                        ',
	'                        ',
	'                        ',
	'                        ',
	'                        ',
	'                        '),

'cardinal' : (         #24x24
	'           ..           ',
	'          .##.          ',
	'         .####.         ',
	'        ...##...        ',#4
	'          .##.          ',
	'          .##.          ',
	'          .##.          ',
	'          .##.          ',#8
	'   .      .##.      .   ',
	'  ..      .##.      ..  ',
	' .#........##........#. ',
	'.##########@###########.',#12
	'.######################.',
	' .#........##........#. ',
	'  ..      .##.      ..  ',
	'   .      .##.      .   ',#16
	'          .##.          ',
	'          .##.          ',
	'          .##.          ',
	'          .##.          ',#20
	'          .##.          ',
	'        ...##...        ',
	'          .##.          ',
	'           ..           '),#24

'horizontal' : (         #24x24
	'         ..  ..         ',
	'        .#.  .#.        ',
	'       .##.  .##.       ',
	'       .##.  .##.       ',#4
	'       .##.  .##.       ',
	'       .##.  .##.       ',
	'       .##.  .##.       ',
	'       .##.  .##.       ',#8
	'   .   .##.  .##.   .   ',
	'  ..   .##.  .##.   ..  ',
	' .#.....##.  .##.....#. ',
	'.#########.@ .#########.',#12
	'.#########.  .#########.',
	' .#.....##.  .##.....#. ',
	'  ..   .##.  .##.   ..  ',
	'   .   .##.  .##.   .   ',#16
	'       .##.  .##.       ',
	'       .##.  .##.       ',
	'       .##.  .##.       ',
	'       .##.  .##.       ',#20
	'       .##.  .##.       ',
	'       .##.  .##.       ',
	'        .#.  .#.        ',
	'         ..  ..         '),#24

'vertical' : (           #24x24
	'           ..           ',
	'          .##.          ',
	'         .####.         ',
	'        ...##...        ',#4
	'          .##.          ',
	'          .##.          ',
	'          .##.          ',
	'  .........##.........  ',#8
	' .####################. ',
	'.######################.',
	'........................',
	'           @            ',#12
	'                        ',
	'........................',
	'.######################.',
	' .####################. ',#16
	'  .........##.........  ',
	'          .##.          ',
	'          .##.          ',
	'          .##.          ',#20
	'        ...##...        ',
	'         .####.         ',
	'          .##.          ',
	'           ..           '),#24

'diag1' : (              #24x24
	'   .....          ......',
	'.   .###.          .###.',
	'..   .###.         .###.',
	'.#.   .###.       .####.',#4
	'.##.   .###.     .###...',
	'.###.   .###.   .###.  .',
	' .###.   .###. .###.    ',
	'  .###.   .###.###.     ',#8
	'   .###.   .#####.      ',
	'    .###.   .###.       ',
	'     .###.   .###.      ',
	'      .###.@  .###.     ',#12
	'       .###.   .###.    ',
	'        .###.   .###.   ',
	'       .#####.   .###.  ',
	'      .###.###.   .###. ',#16
	'     .###. .###.   .###.',
	'    .###.   .###.   .##.',
	'.  .###.     .###.   .#.',
	'...###.       .###.   ..',#20
	'.####.         .###.   .',
	'.###.           .###.   ',
	'.###.            .###.  ',
	'......            ..... '),#24

'diag2' : (              #24x24
	'......          .....   ',
	'.###.          .###.   .',
	'.###.         .###.   ..',
	'.####.       .###.   .#.',#4
	'...###.     .###.   .##.',
	'.  .###.   .###.   .###.',
	'    .###. .###.   .###. ',
	'     .###.###.   .###.  ',#8
	'      .#####.   .###.   ',
	'       .###.   .###.    ',
	'      .###.   .###.     ',
	'     .###. @ .###.      ',#12
	'    .###.   .###.       ',
	'   .###.   .###.        ',
	'  .###.   .#####.       ',
	' .###.   .###.###.      ',#16
	'.###.   .###. .###.     ',
	'.##.   .###.   .###.    ',
	'.#.   .###.     .###.  .',
	'..   .###.       .###...',#20
	'.   .###.         .####.',
	'   .###.           .###.',
	'  .###.            .###.',
	' .....            ......')#24
}


def get_hex(string, trues):

	scale = 8 / len(string)

	n = 0
	for i in range(0, len(string)):
		if string[i] in trues:
			n += pow(2, i*scale)

	for j in range(1, scale):
		n |= n << 1

	if len(hex(n)) == 3:
		return '0x0' + hex(n)[-1] 

	return hex(n)

def get_line_hex(string, trues, scale):

	s_len = 8 / scale

	if len(string) % s_len != 0:
		return -1

	line = ''
	for i in range(0, len(string)/s_len):

		line += get_hex(string[i*s_len:(i+1)*s_len], trues)

		if i < len(string)/s_len - 1:
			line += ','
		else:
			line += '\n'

	k = scale
	while k > 1:
		line += line
		k /= 2

	return line

def generate_single(cursor, scale):

	filename = CWD() + '\Cursors\\' + cursor

	xbm  = '#define cursor_width ' + str(int(24*scale)) + '\n'
	xbm += '#define cursor_height ' + str(int(24*scale)) + '\n'
	xbm += 'static char cursor_bits[] = {\n'

	for line in cursors[cursor]: 
		xbm += get_line_hex(line, ['#'], scale)

	xbm += '};'

	xbm_file = open(filename + '.xbm', 'w')
	xbm_file.write(xbm)
	xbm_file.close()

	xbm_mask  = '#define cursor_width ' + str(int(24*scale)) + '\n'
	xbm_mask += '#define cursor_height ' + str(int(24*scale)) + '\n'
	xbm_mask += 'static char cursor_bits[] = {\n'

	for line in cursors[cursor]: 
		xbm_mask += get_line_hex(line, ['#', '.'], scale)

	xbm_mask += '};'

	xbm_file = open(filename + '_mask.xbm', 'w')
	xbm_file.write(xbm_mask)
	xbm_file.close()

	for line in range(0, len(cursors[cursor])):
		pos = cursors[cursor][line].find("@")
		if pos != -1:
			cursor_offset = (pos * scale, line * scale)
			return cursor + ":" + str(cursor_offset) + ",\n"

	return cursor + ":(0, 0),\n"

def generate():

	scale = SCALE()

	if scale == 3:
		scale = 2

	offsets = open("Cursors\\cursor_offset.txt", "w")
	print offsets
	text = ""

	for cursor in cursors:
		
		text += generate_single(cursor, scale)

	offsets.write(text)
	offsets.close()


class Cursor_Manager(object):

	def __init__(self, start_cursor):

		self.cursors = {}
		self.offsets = {}

		offset_file = open(CWD() + "\Cursors\\cursor_offset.txt", "r")

		for line in offset_file:
			name, value_text = line.split(":")
			value = (int(value_text[1:value_text.find(",")]), int(value_text[value_text.find(",") + 1:value_text.find(")")]))
			self.cursors[name] = pygame.cursors.load_xbm(CWD() + '\Cursors\\' + name + '.xbm', CWD() + '\Cursors\\' + name + '_mask.xbm')
			self.offsets[name] = value

		offset_file.close()

		self.cursor = start_cursor
		pygame.mouse.set_cursor(*self.cursors[self.cursor])
		self.curr_offset = self.offsets[start_cursor]
		

	def set(self, new_cursor, mouse):

		offset_change = [a - b for a, b in zip(self.curr_offset, self.offsets[new_cursor])]
		self.curr_offset = self.offsets[new_cursor]

		self.cursor = new_cursor
		pygame.mouse.set_cursor(*self.cursors[self.cursor])
		pygame.mouse.set_pos([a - b for a, b in zip(mouse["pos"], self.curr_offset)])

	def adjust(self, mouse):

		mouse["pos"] = [a + b for a, b in zip(mouse["pos"], self.curr_offset)]
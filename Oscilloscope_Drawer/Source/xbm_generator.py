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
	'     ##                 ',
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
	'        ##              ',
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
	'.#########.  .#########.',#12
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
	'         ..  ..         ')#24
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

	filename = 'C:\Users\Ben Wilson\Desktop\python_scripts\Oscilloscope_Drawer\Cursors\\' + cursor

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

def generate(scale):

	if scale == 3:
		scale = 2

	for cursor in cursors:
		generate_single(cursor, scale)
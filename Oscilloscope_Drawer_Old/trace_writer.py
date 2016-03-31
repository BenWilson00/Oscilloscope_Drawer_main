from Modules.Basic_h import *
from os import getcwd

CWD = getcwd()

# Command prompt menu
current = 0
quit = False
old_file = 'Oscilloscope_Drawer_Old.ino'

while not quit:
	files = []	
	for file_ in os.listdir(CWD + '\Traces'):
		if file_.endswith('.trace'):
			files.append(file_[:-6])

	option = options_run(files, 0, [['d', 'to select'], ['e', 'to delete'], ['a', 'to exit']], 'Please select the file you want to open.')

	if option[1] == 'e':
		os.remove(CWD + '\Traces\\' + files[option[0]] + str('.trace'))
		files = []	
		for file_ in os.listdir(CWD + '\Traces'):
			if file_.endswith('.trace'):
				files.append(file_[:-6])
		if len(files) == 0:
			break

	elif option[1] == 'a':
		quit = True

	elif option[1] == 'd':
		clear()

		# Write to the arduino file

		filename = str(files[option[0]]) + '.trace'
		data = open(CWD + '\Traces\\' + filename, 'r')

		points_declare = data.read()

		data.close()

		for c in range(21, len(points_declare)):
			if points_declare[c] == ']':
				length = points_declare[21:c]
				break

		length_digits = len(str(length))

		length_to_write = str(length)
		for i in range(0, 10-length_digits):
			length_to_write += ' '

		output = open(old_file, 'r')

		program = output.read()

		output.close()

		stop = 0
		start = 0

		for c in range(0, len(program)):
			if program[c-3:c] == '//~':
				if stop == 0:
					stop = c
				else:
					start = c-3
					break
			elif program[c-11:c-1] == 'NUM_POINTS' and stop == 0:
				num_points_pos = c

		to_write = program[:num_points_pos] + length_to_write + program[num_points_pos+10:stop] + '\n\n' + points_declare[:21] + 'NUM_POINTS' + points_declare[21+length_digits:] + '\n\n' + program[start:]

		output = open(old_file, 'w')

		output.write(to_write)

		output.close()

		print 'Written successfully!'
		exit = raw_input('Please press enter...')
		break
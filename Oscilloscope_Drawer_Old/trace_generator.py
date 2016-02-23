from Modules.Basic_h import *

# Command prompt menu
quit = False

while not quit:

	files = []	
	for file_ in os.listdir('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates'):
		if file_.endswith('.template'):
			files.append(file_[:-9])

	option = options_run(files, 0, [['d', 'to select'], ['e', 'to delete'], ['a', 'to exit']], 'Please select a template to generate a trace for:')

	if option[1] == 'e':
		os.remove('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates\\' + files[option[0]] + str('.template'))
		files = []	
		for file_ in os.listdir('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates'):
			if file_.endswith('.template'):
				files.append(file_[:-9])
		if len(files) == 0:
			break

	elif option[1] == 'a':
		quit = True

	else:
		clear()

		print 'Have some options:'

		gap_user = raw_input('Enter the gap in pixels between each point generated or press enter: ')

		if gap_user == '':
			GAP = 20.0

		else:
			try:
				GAP = float(gap_user)
			except:
				print 'Failed. Setting gap equal to 20.'
				GAP = 20.0

		filename = str(files[option[0]]) + '.template'
		data = open('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates\\' + filename, 'r')

		# Read the file

		line_no = 0
		lines = []
		for line in data:

			lines.append(line)
			line_no += 1

		for line in lines:
			if line[-1] == '\n':
				line = line[:-2]

		points_str = lines[0][10:-2]

		x_value = False
		y_value = False
		x_finish = False
		y_finish = False
		x_value_lst = []
		y_value_lst = []
		current_x_value = ''
		current_y_value = ''

		for c in range(0, len(points_str)):

			if points_str[c-1] == '[':
				x_value = True

			elif points_str[c] == ',' and points_str[c+1] != '[':
				x_finish = True

			elif points_str[c-1] == ',' and points_str[c] != '[':
				y_value = True

			elif points_str[c] == ']':
				y_finish = True

			if x_finish:
				x_value_lst.append(int(current_x_value))
				current_x_value = ''
				x_value = False
				x_finish = False

			elif y_finish:
				y_value_lst.append(int(current_y_value))
				current_y_value = ''
				y_value = False
				y_finish = False

			if x_value:
				current_x_value += points_str[c]

			elif y_value:
				current_y_value += points_str[c]

		points = []

		for p in range(0, len(x_value_lst)):
			points.append([x_value_lst[p], y_value_lst[p]])

		# Generate the list of points for the Arduino program

		newpoints = []

		for p in range(0, len(points)):
			
			distance = float(((points[p][0] - points[p-1][0]) ** 2 + (points[p][1] - points[p-1][1]) ** 2) ** 0.5)
			
			if GAP < distance:

				float_splits = distance / GAP
				low = math.floor(float_splits)
				high = math.ceil(float_splits)
				splits = low if (distance/low - GAP < GAP - distance/high) else high
			
				for i in range(0, int(splits)):
					x = int(i * (points[p][0] - points[p-1][0]) / splits + points[p-1][0])
					y = int(i * (points[p][1] - points[p-1][1]) / splits + points[p-1][1])

					newpoints.append([x,y])

			else:
				newpoints.append(points[p])
		
		data.close()

		filename = files[option[0]] + '.trace'
		output = open('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Traces\\' + filename, 'w')

		to_write = 'unsigned char points[' + str(len(newpoints)) + '][2] = {'
		for p in range(0, len(newpoints)):
			to_write += '{%i,%i}' % (newpoints[p][0]/2, newpoints[p][1]/2)
			if p < len(newpoints) - 1:
				to_write += ','

		to_write += '};'

		output.write(to_write)
		output.close()

		print 'Generated successfully!'
		exit = raw_input('Please press enter...')
		break
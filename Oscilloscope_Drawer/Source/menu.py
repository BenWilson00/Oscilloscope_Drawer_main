import os
from basic import *

def print_options(lst, current):

	for line in range(0, len(lst)):

		if current == line: write('> ')
		else: write('  ')

		write(lst[line] + '\n\n')
		prnt()

def options_run(options, current, additionals, text):
	'''runs a selection loop, returns selected option & user action'''

	while True:

		if current >= len(options):
			current = 0
			
		clear()

		print text + '\n'

		print_options(options, current)

		print '\'s\' to move down, \'w\' to move up,', ', '.join(list('\'' + str(i[0]) + '\' ' + str(i[1]) for i in additionals))


		action = get_input('w', 's', list(i[0] for i in additionals))

		if action == 'w':
			current = (current - 1) % len(options)

		elif action == 's':
			current = (current + 1) % len(options)

		else:
			return [current, action]

def listdir(directory):
	files = []
	for file_ in os.listdir(directory):
		files.append(file_)
	return files

class Menu(object):

	def __init__(self, CWD):
		self.CWD = CWD
		self.output = None

	def delete_file(self, directory):

		while True:

			files = listdir(directory)

			if files != []: action = options_run(files, 0, [['d', 'to delete'] , ['a', 'to exit']], 'Please select a file to delete:')
			else: 
				clear()
				raw_input('No files in this directory. Press enter to return to main menu...')
				break

			if action[1] == 'd':

				os.remove(directory + files[action[0]])
				time.sleep(0.1)


			if action[1] == 'a':

				return 0

	def create_file(self, name, directory, overwrite = False, write='points = [[]]'):

		dup_exists = False

		if not overwrite:

			files = listdir(directory)
			for file_ in files:

				if file_ == name + '.tra':		

					dup_exists = True
					action = options_run(['Overwrite', 'Cancel'], 0, [['d', 'to select']], 'There already exists a file with this name. Cancel or overwrite?')
					
					if action[0] == 0:
						overwrite = True

		if overwrite or not dup_exists:

			new_file = open(directory + name +'.tra', 'w')

			new_file.write(write)

			new_file.close()
			return 0

		else:
			return 1

	def rename_file(self, directory):

		while True:

			files = listdir(directory)

			if files != []: action = options_run(files, 0, [['d', 'to rename'] , ['a', 'to exit']], 'Please select a file to rename:')
			else: 
				clear()
				raw_input('No files in this directory. Press enter to return to main menu...')
				break

			if action[1] == 'd':

				clear()
				name = raw_input('Please enter your new filename for \'' + files[action[0]] +'\':\n').lower()

				if len(name) > 20:
					name = name[:20]
				if name + '.tra' == files[action[0]]:
					pause = raw_input('You cannot give the file the same name. Press enter to return...')
					continue

				copyfile = open(directory + files[action[0]], 'r')
				create_file(name, directory, False, copyfile.read())
				copyfile.close()

				os.remove(directory + files[action[0]])


			if action[1] == 'a':

				return 0

	def write_file(self, directory):

		files = listdir(directory)

		if files != []: action = options_run(files, 0, [['d', 'to write'] , ['a', 'to exit']], 'Please select a file to write:')

		if action[1] == 'd':

			clear()

			error = Writer.write_to_arduino(directory + files[action[0]])

			if error == 0:
				pause = raw_input('Written successfully. Press enter to return to main menu...')
				return 0
			else:
				pause = raw_input('Writing error: ' + str(error) + '. Press enter to return to main menu...')
				return 1

		if action[1] == 'a':
			return 0

	def open_file(self, directory):

		files = listdir(directory)

		if files != []: action = options_run(files, 0, [['d', 'to open'] , ['a', 'to exit']], 'Please select a file to open:')

		if action[1] == 'd':

			return files[action[0]]

		if action[1] == 'a':
			return 0

	def run_menu(self):
		'''runs the main menu for the oscilloscope drawer program'''

		files_there = False
		for file_ in os.listdir(self.CWD+'\Traces'):
			files_there = True
			break

		if files_there:
			option_list = ['Open file', 'Create file', 'Write file', 'Delete file', 'Rename file']
		else:
			option_list = ['Create file']


		action = options_run(option_list, 0, [['d', 'to select'] , ['a', 'to exit']], 'Please select an action:')

		if action[1] == 'd':

			clear()

			if option_list[action[0]] == 'Rename file':

				self.rename_file(self.CWD + '\Traces\\')
				self.output = None

			elif option_list[action[0]] == 'Delete file':

				self.delete_file(self.CWD + '\Traces\\')
				self.output = None

			elif option_list[action[0]] == 'Write file':

				self.write_file(self.CWD + '\Traces\\')
				self.output = None

			elif option_list[action[0]] == 'Open file':

				self.output = self.open_file(self.CWD + '\Traces\\')

			elif option_list[action[0]] == 'Create file':
				
				name = raw_input('Please enter your filename:\n').lower()

				if len(name) > 20:
					name = name[:20]

				self.create_file(name, self.CWD + '\Traces\\')
				self.output = None
				#Trace = open_file()
				#return Trace

		elif action[1] == 'a':
			self.output = 0
import time, math, random, subprocess, platform, time, msvcrt, sys, glob, os
from random import randint
from pygame.locals import *

def get_input(*args):
	userResponse = ''
	while userResponse not in args and userResponse not in args[-1]:
		userResponse = msvcrt.getch()
	return userResponse

def clear():
	subprocess.Popen('cls' if platform.system() == 'Windows' else 'clear', shell=True)
	time.sleep(0.02)

def write(string):
	sys.stdout.write(string)

def prnt():
	sys.stdout.flush()

def print_options(lst, current):

	for line in range(0, len(lst)):

		if current == line: write('> ')
		else: write('  ')

		write(lst[line] + '\n')
		prnt()

def options_run(options, current, additionals, text):
	'''runs a selection loop, returns selected option & user action'''

	while True:

		if current >= len(options):
			current = 0
			
		clear()

		print text + '\n'

		print_options(options, current)

		print '\n\'s\' to move down, \'w\' to move up,', ', '.join(list('\'' + str(i[0]) + '\' ' + str(i[1]) for i in additionals))


		action = get_input('w', 's', list(i[0] for i in additionals))

		if action == 'w':
			current = (current - 1) % len(options)

		elif action == 's':
			current = (current + 1) % len(options)

		else:
			return [current, action]
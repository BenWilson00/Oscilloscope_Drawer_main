import os
import pygame
from pygame.locals import *
from Source import *

import ctypes

ctypes.windll.user32.SetProcessDPIAware()

SETCWD(os.getcwd())
print '\nCWD: ' + CWD() + '\n'

time.sleep(0.5)
clear()

while True:

	# Handle main menu & its output

	main_menu = Menu(CWD())

	while main_menu.output == None:
		main_menu.run_menu()
	
	if main_menu.output == 0: exit(0)

	# Initialise program aspects

	trace_file = open(CWD() + '\Traces\\' + main_menu.output, 'r')

	lines = []
	for line in trace_file:
		lines.append(line.rstrip('\n'))

	trace_file.close()

	trace = Trace(lines)

	editor = Editor(trace, main_menu.output)

	clear()

	# Run program loop

	quit = False
	
	while not quit:

		editor.update()
		
		editor.draw()


 	pygame.display.update()
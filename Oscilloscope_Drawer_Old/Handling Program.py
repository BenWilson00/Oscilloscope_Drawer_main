from Modules.Basic_h import *

# Command prompt menu

time.sleep(0.2)

quit_program = False

drawing_program_opened = False
trace_generator_opened = False
trace_writer_opened = False

options = ['Go to template editing program']

for file_ in os.listdir('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates'):
	options.append('Generate a trace from a template')
	break

for file_ in os.listdir('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates'):
	options.append('Write a generated trace to the arduino program')
	break

while not quit_program:

	option = options_run(options, 0, [['d', 'to select'] , ['a', 'to exit']], 'Please select an action:')

	if option[1] == 'a':
		quit_program = True

	else:
		if option[0] == 0:
			clear()
			if not drawing_program_opened:
				import drawing_program
				drawing_program_opened = True
			else:
				drawing_program = reload(drawing_program)

		elif options[option[0]] == 'Generate a trace from a template':
			clear()
			if not trace_generator_opened:
				import trace_generator
				trace_generator_opened = True
			else:
				trace_generator = reload(trace_generator)

		elif options[option[0]] == 'Write a generated trace to the arduino program':
			clear()
			if not trace_writer_opened:
				import trace_writer
				trace_writer_opened = True
			else:
				trace_writer = reload(trace_writer)

if drawing_program_opened: os.remove('drawing_program.pyc')
if trace_generator_opened: os.remove('trace_generator.pyc')
if trace_writer_opened: os.remove('trace_writer.pyc')
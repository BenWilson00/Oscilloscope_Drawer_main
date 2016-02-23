import time, subprocess, platform, msvcrt, sys, math
from point import *

def get_input(*args):
	userResponse = ''
	while userResponse not in args and userResponse not in args[-1]:
		userResponse = msvcrt.getch()
	return userResponse

def clear(sleeptime=0.02):
	subprocess.Popen('cls' if platform.system() == 'Windows' else 'clear', shell=True)
	if sleeptime > 0: time.sleep(sleeptime)

def write(string):
	sys.stdout.write(string)

def prnt():
	sys.stdout.flush()

def pause(reason=''):
	if reason != '': raw_input('Paused with message : \n'+reason + '\nPress enter to resume.')
	else: raw_input('Paused. Press enter to resume.')

def add_tuple(*args):
	return_tup = ()
	for i in range(0, len(args[0])):
		summed = 0
		for tup in args:
			summed += tup[i]
		return_tup += (summed,)
	return return_tup

def subtract_tuple(*args):
	return_tup = ()
	for i in range(0, len(args[0])):
		summed = args[0][i]
		for tup in range(1, len(args)):
			summed -= args[tup][i]
		return_tup += (summed,)
	return return_tup

def multiply_tuple(arg1, arg2, **kwargs):
	if type(arg1) == tuple and type(arg2) == tuple:
		return_tup = ()

		for value in range(0, len(arg1)):
			multiplied = int(round(arg1[value]*arg2[value])) if 'int' in kwargs else arg1[value]*arg2[value]
			return_tup += (multiplied,)

		return return_tup
		
	elif type(arg1) != tuple:
		return_tup = ()

		for value in arg2:
			multiplied = int(round(arg1*value)) if 'int' in kwargs else arg1*value
			return_tup += (multiplied,)

		return return_tup

def divide_tuple(arg1, arg2, **kwargs):
	if type(arg1) == tuple and type(arg2) == tuple:
		return_tup = ()

		for value in range(0, len(arg1)):
			multiplied = int(round(arg1[value]/arg2[value])) if 'int' in kwargs else arg1[value]/float(arg2[value])
			return_tup += (multiplied,)

		return return_tup
		
	elif type(arg1) != tuple:
		return_tup = ()

		for value in arg2:
			multiplied = int(round(arg1/value)) if 'int' in kwargs else arg1/float(value)
			return_tup += (multiplied,)

		return return_tup
	return_tup = ()

def convert_str_tuple_to_tuple(string, **kwargs):
	value_type = kwargs['type'] if 'type' in kwargs else str
	string = string[1:-1]
	values = ()
	for value in string.split(','):
		if value != '':
			values += (value_type(value),)

	return values

def convert_str_list_to_list(string, **kwargs):
	value_type = kwargs['type'] if 'type' in kwargs else str
	string = string[1:-1]
	values = []
	for value in string.split(','):
		if value != '':
			values.append(value_type(value))

	return values

sign = lambda x: math.copysign(1, x)

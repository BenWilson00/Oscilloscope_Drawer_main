import time, subprocess, platform, msvcrt, sys, math
from point import *

SCALE_VALUE = 1.0

def SCALE():
	return SCALE_VALUE

def SETSCALE(value):
	global SCALE_VALUE
	SCALE_VALUE = value

CWD_VALUE = 1.0

def CWD():
	return CWD_VALUE

def SETCWD(value):
	global CWD_VALUE
	CWD_VALUE = value

def scaleup(*values):
	if len(values) == 1 and (type(values[0]) == tuple or type(values[0])):
		return multiply_tuple(SCALE(), values[0])
	elif len(values) > 1:
		return multiply_tuple(SCALE(), values)
	else:
		return SCALE() * values[0]

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
		
	elif type(arg2) != tuple:
		return_tup = ()

		for value in arg1:
			multiplied = int(round(value/arg2)) if 'int' in kwargs else float(value)/float(arg2)
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

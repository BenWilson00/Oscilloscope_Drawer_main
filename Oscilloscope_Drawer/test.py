keys = {'Button1' : [['Lmouse', 'ctrl'], ['Rmouse']],
		'Button2' : [['Lmouse'], ['Rmouse', 'shift']]}

for key in keys:
	print key + ' = [' + reduce(lambda x, y : x + ',' + y, keys[key][0]) + '],[' + reduce(lambda x, y : x + ',' + y, keys[key][1]) + ']'

def convert_str_list_to_list(string, **kwargs):
	value_type = kwargs['type'] if 'type' in kwargs else str
	string = string[1:-1]
	values = []
	for value in string.split(','):
		if value != '':
			values.append(value_type(value))

	return values

text = '[Lmouse],[Rmouse,ctrl]'

split = [text[:text.index(',')], text[text.index(',') + 1:]]

for value in split:
	print convert_str_list_to_list(value)
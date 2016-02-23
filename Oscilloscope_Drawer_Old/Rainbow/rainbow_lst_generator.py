rainbow_cols = [[255, 0, 0], [255, 127, 0], [255, 255, 0], [0, 255, 0], [0, 0, 255], [75, 0, 130], [139, 0, 255]]

# 255/7 = 36 r 3

rainbow_lst = []

for i in range(0, 3):
	rainbow_lst.append([0, 0, 0])

end_rainbow_lst = []
for i in range(0, 252):
	colours = [rainbow_cols[i/36 - 1], rainbow_cols[i/36]]
	col = [0, 0, 0]
	for j in range(0, len(col)):

		col[j] = int((i/252.0) * (colours[0][j] - ((i % 36) * (colours[0][j] - colours[1][j]))/36))
	end_rainbow_lst.append(col)	

myfile = open('rainbow_lst', 'w')

for i in end_rainbow_lst:
	rainbow_lst.append(i)

string = '['
for i in range(0, len(rainbow_lst)):
	string += str(rainbow_lst[i])

	if i < 254:
		string += ', '

	if (i - 2) % 36 == 0 and i < 254:
		string += '\n'

string += ']'


myfile.write(string)


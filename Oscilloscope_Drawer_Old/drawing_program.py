from Modules.Basic_h import *
from Modules.Drawer_h import *

WIDTH = 900
HEIGHT = 800
SCREEN_SIZE = [WIDTH, HEIGHT]

traces = []

no_file = True
click = False
rightclick = False
add_point_click = False
clicked = 0

tracing = False
total_iterations = 0
trace_iteration = 0
n_trace_particles = 0
trace_particles = []

buttons = [Button([20, 20], 'save', False),
		   Button([WIDTH-60, 20], '+', False), 
		   Button([WIDTH-20, 20], '-', False),
		   Button([20, HEIGHT-20], '>', False),
		   Button([60, HEIGHT-20], '||', False),
		   Button([WIDTH-60, HEIGHT-20], '+', False), 
		   Button([WIDTH-20, HEIGHT-20], '-', False)]

burst = 0
burst_particles = []
rainbow_lst = [[0, 0, 0], [0, 0, 0], [0, 0, 0], 
			   [0, 0, 0], [0, 0, 0], [1, 0, 1], [1, 0, 2], [2, 0, 3], [3, 0, 4], [3, 0, 5], [4, 0, 5], [5, 0, 6], [6, 0, 6], [6, 0, 7], [7, 0, 7], [8, 0, 8], [9, 0, 8], [10, 0, 8], [11, 0, 8], [12, 0, 9], [13, 0, 9], [14, 0, 9], [15, 0, 9], [16, 0, 9], [17, 0, 8], [18, 0, 8], [19, 0, 8], [20, 0, 8], [21, 0, 7], [23, 0, 7], [24, 0, 6], [25, 0, 6], [26, 0, 5], [28, 0, 5], [29, 0, 4], [30, 0, 3], [32, 0, 2], [33, 0, 2], [35, 0, 1], 
			   [36, 0, 0], [37, 0, 0], [38, 1, 0], [39, 1, 0], [40, 2, 0], [41, 2, 0], [42, 3, 0], [43, 4, 0], [44, 5, 0], [45, 5, 0], [46, 6, 0], [47, 7, 0], [48, 8, 0], [49, 8, 0], [50, 9, 0], [51, 10, 0], [52, 11, 0], [53, 12, 0], [54, 13, 0], [55, 14, 0], [56, 15, 0], [57, 16, 0], [58, 17, 0], [59, 19, 0], [60, 20, 0], [61, 21, 0], [62, 22, 0], [63, 24, 0], [64, 25, 0], [65, 26, 0], [66, 27, 0], [67, 29, 0], [68, 30, 0], [69, 32, 0], [70, 33, 0], [71, 34, 0], 
			   [72, 36, 0], [73, 37, 0], [74, 39, 0], [75, 41, 0], [76, 42, 0], [77, 44, 0], [78, 46, 0], [79, 47, 0], [80, 49, 0], [81, 51, 0], [82, 53, 0], [83, 55, 0], [85, 56, 0], [86, 58, 0], [87, 60, 0], [88, 62, 0], [89, 64, 0], [90, 66, 0], [91, 68, 0], [92, 70, 0], [93, 72, 0], [94, 74, 0], [95, 76, 0], [96, 78, 0], [97, 81, 0], [98, 83, 0], [99, 85, 0], [100, 87, 0], [101, 90, 0], [102, 92, 0], [103, 94, 0], [104, 97, 0], [105, 99, 0], [106, 102, 0], [107, 104, 0], [108, 107, 0], 
			   [109, 109, 0], [107, 110, 0], [105, 111, 0], [103, 112, 0], [100, 113, 0], [98, 114, 0], [96, 115, 0], [94, 116, 0], [91, 117, 0], [89, 118, 0], [86, 119, 0], [84, 120, 0], [80, 121, 0], [78, 122, 0], [75, 123, 0], [72, 124, 0], [69, 125, 0], [66, 126, 0], [64, 127, 0], [60, 128, 0], [57, 129, 0], [54, 130, 0], [51, 131, 0], [48, 132, 0], [44, 133, 0], [41, 134, 0], [37, 135, 0], [34, 136, 0], [30, 137, 0], [27, 138, 0], [23, 139, 0], [19, 140, 0], [16, 141, 0], [12, 142, 0], [8, 143, 0], [4, 144, 0], 
			   [0, 145, 0], [0, 142, 4], [0, 139, 8], [0, 136, 12], [0, 133, 17], [0, 130, 21], [0, 126, 25], [0, 123, 29], [0, 120, 34], [0, 116, 38], [0, 113, 43], [0, 109, 47], [0, 105, 52], [0, 101, 57], [0, 97, 62], [0, 94, 67], [0, 90, 72], [0, 86, 77], [0, 82, 82], [0, 78, 87], [0, 74, 92], [0, 70, 97], [0, 65, 102], [0, 61, 108], [0, 56, 113], [0, 52, 119], [0, 47, 124], [0, 43, 130], [0, 38, 135], [0, 34, 141], [0, 29, 147], [0, 25, 152], [0, 20, 158], [0, 15, 164], [0, 10, 170], [0, 5, 176], 
			   [0, 0, 182], [2, 0, 181], [3, 0, 179], [5, 0, 177], [6, 0, 176], [8, 0, 174], [9, 0, 173], [11, 0, 171], [12, 0, 170], [14, 0, 168], [15, 0, 166], [17, 0, 164], [19, 0, 163], [21, 0, 160], [23, 0, 159], [24, 0, 157], [26, 0, 155], [28, 0, 153], [29, 0, 151], [31, 0, 150], [33, 0, 147], [35, 0, 145], [36, 0, 143], [38, 0, 141], [40, 0, 139], [43, 0, 137], [44, 0, 134], [46, 0, 133], [48, 0, 130], [50, 0, 128], [52, 0, 125], [54, 0, 123], [56, 0, 121], [58, 0, 119], [60, 0, 116], [62, 0, 114], 
			   [64, 0, 111], [66, 0, 115], [68, 0, 118], [70, 0, 122], [72, 0, 125], [73, 0, 129], [75, 0, 133], [77, 0, 137], [80, 0, 140], [81, 0, 144], [83, 0, 147], [85, 0, 152], [87, 0, 155], [89, 0, 159], [91, 0, 163], [93, 0, 167], [95, 0, 171], [98, 0, 175], [99, 0, 179], [101, 0, 182], [103, 0, 187], [106, 0, 190], [108, 0, 195], [110, 0, 199], [112, 0, 203], [114, 0, 207], [117, 0, 212], [118, 0, 216], [121, 0, 220], [123, 0, 224], [125, 0, 229], [128, 0, 233], [129, 0, 238], [132, 0, 242], [134, 0, 247], [0, 255, 0]]
rainbow = False


# Command prompt menu

files_there = False
for file_ in os.listdir('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates'):
	files_there = True
	break

if files_there:
	options = ['Create file', 'Open file']
else:
	options = ['Create file']

time.sleep(0.2)

quit_program = False
while not quit_program:

	option = options_run(options, 0, [['a', 'to quit'], ['d', 'to select']], 'Would you like to open a file or create a new one?')

	if option[1] == 'a':
		quit_program = True

	elif option[1] == 'd':

		clear()

		return_to_menu = False

		if option[0] == 0:

			speed = 15
			trail_length = 10
			points = [Point([WIDTH/2, 50], 0)]

			filename = raw_input('Please enter the name of your file:\n')
			filename += '.template'

			doc = open('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates\\' + filename, 'w')
			no_file = False

		elif option[0] == 1:

			while not return_to_menu:

				files = []	
				for file_ in os.listdir('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates'):
					files.append(file_[:-9])

				option = options_run(files, 0, [['a', 'to quit'], ['d', 'to select'], ['e', 'to delete file']], 'Please select a file:')

				if option[1] == 'e':
					os.remove('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates\\' + files[option[0]] + str('.template'))
					files = []	
					for file_ in os.listdir('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates'):
						if file_.endswith('.template'):
							files.append(file_[:-9])
						if len(files) == 0:
							return_to_menu = True
							break

				elif option[1] == 'a':
					return_to_menu = True
					break

				elif option[1] == 'd':
					filename = str(files[option[0]]) + '.template'
					data = open('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates\\' + filename, 'r')
					no_file = False
					clear()
					break

			if not return_to_menu:

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
					points.append(Point([x_value_lst[p], y_value_lst[p]], p))

				speed = float(lines[1][8:])
				trail_length = int(lines[2][15:])

				data.close()
				doc = open('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates\\' + filename, 'w')
				no_file = False

		if not (no_file or return_to_menu):

			display = pygame.display.set_mode(SCREEN_SIZE)
			pygame.mouse.set_visible(1)

			iteration = 0

			while not quit_program:

				iteration += 1

				if clicked != 0:
					still_clicked = True
					point_clicked = clicked
					clicked = 0
				else:
					still_clicked = False

				mouse = pygame.mouse.get_pos()
				events = pygame.event.get()

				for event in events:
					if event.type == pygame.QUIT:
						quit_program = True
						break
					elif event.type == MOUSEBUTTONDOWN:
						if event.button != 3:
							click = True
						else:
							rightclick = True
					elif event.type == MOUSEBUTTONUP:
						if event.button == 1:
							click = False
						else:
							rightclick = False
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE and tracing:
							burst = 30
						if tracing:
							rainbow = True

				display.fill((0, 0, 0))

				# Check for points pressed

				to_pop = -1
				for p in range(0, len(points)):
					if not still_clicked or p == point_clicked - 1:
						output = points[p].check_pressed(mouse, click, rightclick)
						if output == 'click':
							clicked = p + 1
						elif output == 'pop':
							to_pop = p

				if to_pop >= 0 and len(points) > 0:
					points.pop(to_pop)

				# Check for buttons pressed

				for b in range(0, len(buttons)):
					if not still_clicked:
						if buttons[b].check_pressed(mouse, click):
							clicked = -(b + 1)

				if clicked == 0 and click and not tracing:

					if len(points) > 1:
						distance_lst =  {}
						for p in range(0, len(points)):

							x_dif = float(points[p].pos[0] - points[p-1].pos[0])
							y_dif = float(points[p].pos[1] - points[p-1].pos[1])

							if (not (x_dif <= 3 and x_dif >= -3)) and (y_dif > 0 or y_dif < 0):
								line1_m =  y_dif / x_dif
								line1_c = points[p].pos[1] + y_dif - line1_m * (points[p].pos[0] + x_dif)
								line2_m = -1/line1_m
								line2_c = mouse[1] - line2_m * mouse[0]
								x_intercept = int((line1_c - line2_c) /  (line2_m - line1_m))
								y_intercept = int(line1_m * x_intercept + line1_c)
							
								if (points[p-1].pos[0] <= x_intercept <= points[p].pos[0] or points[p-1].pos[0] >= x_intercept >= points[p].pos[0]) and (points[p-1].pos[1] <= y_intercept <= points[p].pos[1] or points[p-1].pos[1] >= y_intercept >= points[p].pos[1]):
									distance_lst[p] = [[abs(mouse[0] - x_intercept), abs(mouse[1] - y_intercept)], [x_intercept, y_intercept]]

							elif x_dif <= 3 and x_dif >= -3:
								x_intercept = points[p].pos[0]
								y_intercept = mouse[1]

								if (points[p-1].pos[0] <= x_intercept <= points[p].pos[0] or points[p-1].pos[0] >= x_intercept >= points[p].pos[0]) and (points[p-1].pos[1] <= y_intercept <= points[p].pos[1] or points[p-1].pos[1] >= y_intercept >= points[p].pos[1]):
									distance_lst[p] = [[abs(mouse[0] - x_intercept), abs(mouse[1] - y_intercept)], [x_intercept, y_intercept]]

							elif y_dif == 0:
								x_intercept = mouse[0]
								y_intercept = points[p].pos[1]

								if (points[p-1].pos[0] <= x_intercept <= points[p].pos[0] or points[p-1].pos[0] >= x_intercept >= points[p].pos[0]) and (points[p-1].pos[1] <= y_intercept <= points[p].pos[1] or points[p-1].pos[1] >= y_intercept >= points[p].pos[1]):
									distance_lst[p] = [[abs(mouse[0] - x_intercept), abs(mouse[1] - y_intercept)], [x_intercept, y_intercept]]

						if not add_point_click:
							add_point_click = True
							smallest = [40, -1]
							for l, i in distance_lst.iteritems(): 
								hyp = (i[0][0]**2 + i[0][1]**2)**0.5
								if hyp < smallest[0]:
									smallest[0] = hyp
									smallest[1] = l
							if smallest[1] >= 0:
								points.insert(smallest[1], Point(mouse, len(points)))

					elif (not (mouse[0] < 80 and mouse[1] < 40)) and (not (mouse[0] > WIDTH - 80 and mouse[1] < 40)) and (not (mouse[0] < 80 and mouse[1] > HEIGHT - 40)) and (not (mouse[0] > WIDTH - 80 and mouse[1] > HEIGHT - 40)):
						points.append(Point(mouse, len(points)))

				if not click and add_point_click:
					add_point_click = False

				#Carry out click scenarios

				# Move point
				if clicked > 0 and not tracing:
					points[clicked - 1].pos = mouse

				# Save file
				elif clicked == -1 or iteration == 10:
					to_write = 'points = ['
					for p in range(0, len(points)):
						to_write += '[%i,%i]' % (points[p].pos[0], points[p].pos[1])
						if p < len(points) - 1:
							to_write += ','

					to_write += ']\nspeed = %i.0\ntrail length = %i' % (int(speed), trail_length)

					doc.close()
					doc = open('C:\Users\Benjamin\Desktop\python_scripts\Oscilloscope_Drawer_Copy\Templates\\' + filename, 'w')
					doc.write(to_write)
					print 'Saved to file \'' + filename + '\''



				# Speed adjustment
				elif clicked == -2:
					clear()
					speed += round(speed/20) + 1
					print 'speed = ' + str(speed)

				elif clicked == -3 and speed > 1:
					clear()
					speed -= round(speed/20) + 1
					print 'speed = ' + str(speed)

				# Play button
				elif clicked == -4 and len(points) > 1 or trace_iteration >= len(trace_particles) and tracing:
					tracing = True
					start_trace_time = iteration

					length = calc_trace_length(points)

					trace_particles = []

					n_trace_particles = int(5000 / float(speed))

					trace_iteration = 0
					trace_path(points, trace_particles, trace_iteration, length, n_trace_particles, trail_length)

				# Pause button
				elif clicked == -5 and len(points) > 1:
					tracing = False
					trace_particles = []
					rainbow = False

				elif clicked == -6:
					clear()
					if trail_length >= 15:
						print 'The trail length is at maximum.'
					else:
						trail_length += 1
						print 'trail length = ' + str(trail_length)	

				elif clicked == -7 :
					clear()
					if trail_length > 1:
						trail_length -= 1
						print 'trail length = ' + str(trail_length)
					else:
						print 'The trail length is at minumum.'

				if tracing:
				#Mimic oscilloscope

					trace_iteration = iteration - start_trace_time

					for t in range(0, len(trace_particles)):
						if (trace_iteration + len(trace_particles)) < trace_particles[t].killtime and trace_iteration < trace_particles[-t].lifetime:
							trace_particles[t].draw(trace_iteration, len(trace_particles), display, rainbow_lst, rainbow, iteration)
				
					for t in range(0, len(trace_particles)):
						if trace_particles[t].starttime <= trace_iteration and trace_particles[t].killtime >= trace_iteration:
							trace_particles[t].draw(trace_iteration, len(trace_particles), display, rainbow_lst, rainbow, iteration)

				else:
				#Draw connection lines
					for p in range(0, len(points)):
						pygame.draw.line(display, (0, 255, 0), points[p-1].pos, points[p].pos, 1)

				if burst > 0 and tracing:

					if burst % 3 == 0:

						size = randint(1,4)
						for i in range(0, randint(10, 30)):

							v = [randint(-30, 30), randint(-30, 30)]
							colour = [randint(0, 255), randint(0, 255), randint(0, 255)]
							i_lifetime = randint(20, 40)

							burst_particles.append(RainbowSpark([trace_particles[trace_iteration - 1].pos[0], trace_particles[trace_iteration - 1].pos[1]], v, colour, size, iteration, i_lifetime))

					burst -= 1

				for p in points:
					p.draw(tracing, display)

				for b in buttons:
					b.draw(display)

				pop_lst = []
				for b in range(0, len(burst_particles)):
					burst_particles[b].update(iteration)
					burst_particles[b].draw(display)
					if iteration > burst_particles[b].killtime + randint(20, 40):
						pop_lst.append(b)

				for b in range(1, len(pop_lst)+1):
					burst_particles.pop(pop_lst[-b])

				pygame.display.flip()

if not no_file:
	doc.close()

pygame.display.quit()
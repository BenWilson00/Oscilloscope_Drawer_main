import PIL
from PIL import Image
import numpy as np

def find_edge(a, start=0):
  print "finding edges"
  for i in range(start, len(a)):
    for j in range(len(a[i])):
      if a[i][j] == 255:
        return i, j

  print "no more edges"
  return -1


def clip(a, b):
  return min(len(a) - 1, max(0, b))

def find_direction(a, x, y, r, threshold):

  donot_erase_dict = {0:(1,3,2,5), 1:(0,2,3,4), 2:(1,4,0,7),
                      3:(0,5,1,6),              4:(2,7,1,6),
                      5:(3,6,0,7), 6:(5,7,3,4), 7:(4,6,2,5)}

  d = 2*r - 1

  #print r, threshold

  x1 = max(0, x - (r-1))
  y1 = max(0, y - (r-1))

  #print x1,y1

  cellstarts = [[x1-d, y1-d], [x1-d, y1], [x1-d, y1+d],
                 [x1, y1-d],               [x1, y1+d],
                [x1+d, y1-d], [x1+d, y1], [x1+d, y1+d]]

  max_total = 0
  direction = -1
  for k in range(len(cellstarts)):
    start = cellstarts[k]

    total = 0

    for i in range(clip(a, start[0]), clip(a, start[0]+d)):
      for j in range(clip(a[0], start[1]), clip(a[0], start[1]+d)):
        total += a[i][j]
        a[i][j] = 0


    #print start, total/255

    if total > max_total:
      max_total = total
      direction = k

  #print direction

  #erase lines
  if direction != -1:

    for i in range(clip(a, x1), clip(a, x1+d)):
      for j in range(clip(a[0], y1), clip(a[0], y1+d)):
        a[i][j] = 0

    for k in range(len(cellstarts)):
      if k not in donot_erase_dict[direction]:

        start = cellstarts[k]
        for i in range(clip(a, start[0]), clip(a, start[0]+d)):
          for j in range(clip(a[0], start[1]), clip(a[0], start[1]+d)):
            a[i][j] = 0

  if max_total > threshold and direction != -1:
    #print "new", clip(a, cellstarts[direction][0] + r - 1), clip(a[0], cellstarts[direction][1] + r - 1)
    return clip(a, cellstarts[direction][0] + r - 1), clip(a[0], cellstarts[direction][1] + r - 1)
  else:
    return -1


START_R = 3
START_THRESHOLD = 0
END_R = 7
END_THRESHOLD = 10

JUMP_LENGTH = 5


with PIL.Image.open("dickbutt.png") as img:

  pxl_map = img.load()

  a = [[0 for j in range(img.size[0])] for i in range(img.size[1])]

  for j in range(img.size[0]):
      for i in range(img.size[1]):
          a[i][j] = pxl_map[j,i]

  ## find a white pixel
  first_edge = find_edge(a)

  #iter = 0
  last_x, last_y = -1, -1
  trails = []

  ## follow path of nearby white pixels, building an array of points visited
  while first_edge != -1:

    x, y = first_edge

    curr_trail = []
    curr_trail.append((x, y))

    ## if it's stuck in a loop, set the pixels it's stuck on to black
    if last_x == x and last_y == y:
      a[x][y] = 0

    newstart = find_direction(a, x, y, START_R, START_THRESHOLD)
    
    
    ## if no white pixel is found, increase leniency up to a maximum radius and minimum number of pixels threshold
    while newstart != -1:
      
      #iter += 1
      x, y = newstart
      
      curr_trail.append((x, y))

      i = 0
      while True:

        #print "r", START_R + i, "t", START_THRESHOLD +int((END_THRESHOLD - START_THRESHOLD) * i/float(END_R - START_R))

        newstart = find_direction(a, x, y, START_R + i, START_THRESHOLD +int((END_THRESHOLD - START_THRESHOLD) * (START_R  + i)/float(END_R)))

        if newstart == -1:
          i += 1
          if START_R + i > END_R:
            curr_trail.append((x, y))
            break
        else:
          i = 0
          break

      #Image.fromarray(np.uint8(a)).show()

    trails.append(curr_trail)
    last_x, last_y = x, y
   
    #Image.fromarray(np.uint8(a)).show()

    first_edge = find_edge(a, first_edge[0])
    

  # im2 = Image.fromarray(np.uint8(a))
  i = 0
  while i < len(trails):
    if len(trails[i]) <= 3:
      trails.pop(i)
    else:
      i += 1

  for trail in trails:

    i = 0
    for point in trail:
      #a[point[0]][point[1]] = 120
      i += 1
      if i % JUMP_LENGTH == 1:
        a[point[0]][point[1]] = 255
      if i > len(trail) - JUMP_LENGTH/2 - 1:
        print i, len(trail) - JUMP_LENGTH/2 - 1
        a[trail[len(trail)-1][0]][trail[len(trail)-1][1]]

  Image.fromarray(np.uint8(a)).show()
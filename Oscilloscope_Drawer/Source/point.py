import math
from point import *

class Point(object):

	def __init__(self, pos = (0, 0)):
		self.x, self.y = map(float, pos)

	def __add__(self, point2):
		return Point((self.x + point2.x, self.y + point2.y))

	def __sub__(self, point2):
		return Point((self.x - point2.x, self.y - point2.y))

	def __mul__(self, scalar):
		return Point((self.x * scalar, self.y * scalar))

	def __div__(self, scalar):
		return Point((self.x / scalar, self.y / scalar))

	def __len__(self, **kwargs):
		return int(round(math.sqrt(self.x**2 + self.y**2)))  if 'int' in kwargs else math.sqrt(self.x**2 + self.y**2)

	def x_between(self, a, b, inequality = '>=/<='):
		if (type(a) == float or type(a) == int) and (type(b) == float or type(a) == int):
			if inequality == '>/<':
				if a < self.x < b or b < self.x < a:
					return True
			elif inequality == '>=/<=':
				if a <= self.x <= b or b <= self.x <= a:
					return True

	def y_between(self, a, b, inequality = '>=/<='):
		if (type(a) == float or type(a) == int) and (type(b) == float or type(a) == int):
			if inequality == '>/<':
				if a < self.y < b or b < self.y < a:
					return True
			elif inequality == '>=/<=':
				if a <= self.y <= b or b <= self.y <= a:
					return True

	def i_tup(self):
		return map(lambda x: int(round(x)), (self.x, self.y)) 

	def tup(self):
		return (self.x, self.y)
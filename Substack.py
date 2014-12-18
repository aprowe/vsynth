from Stack import *
from Latchable import *

class Substack(Stack, Latchable):

	def __init__(s):
		Stack.__init__(s)
		Latchable.__init__(s)

	def append_array(s, latchable, count):
		[s.append(latchable()) for i in range(count)]
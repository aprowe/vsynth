import Stack, Latchable

class Substack(Stack, Latchable):

	def __init__(s):
		Stack.__init__(s)
		Latchable.__init__(s)

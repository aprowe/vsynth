class CDict(dict):

	def init(self):
		super().__init__()

	def __call__(self):
		c = CDict()
		for key, value in self.items():
			if type(value) is dict:
				value = CDict(value)

			if callable(value):
				value = value()

			c[key] = value
		return c

	def reduce(self):
		c = {}
		for key, value in self.items():
			c[key] = self.reduceItem(value)
		return CDict(c)

	def reduceItem(self, value):
		if type(value) is list: 
			fn = value[0]
			attr = lambda: getattr(self, value[0])

			if callable(attr()):
				params = {} if len(value) is 1 else value[1]
				params = CDict(params).reduce3()
				# params = self.reduceItem(value[1])
				return lambda: attr()(**params())
			else: 
				return attr


		if callable(value):
			return value

		return lambda: value

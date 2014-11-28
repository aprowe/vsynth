class CDict(dict):

	def init(self):
		super(CDict, self).__init__()

	def eval(self):
		c = CDict()
		for key, value in self.items():
			if type(value) is dict:
				value = CDict(value)

			if callable(value):
				value = value()

			c[key] = value
		return c


	def reduce(self,target):
		c = {}
		for key, value in self.items():
			c[key] = self.reduceItem(value, target)
		return CDict(c)

	def reduceItem(self, value, target):
		if type(value) is list: 
			fn = value[0]
			attr = lambda: getattr(target, value[0])

			if callable(attr()):
				params = {} if len(value) is 1 else value[1]
				params = CDict(params).reduce(target)
				return lambda: attr()(**params.eval())
			else: 
				return attr


		if callable(value):
			return value

		return lambda: value


def formatLatch(dic):
	source = dic['source']
	target = dic['target']
	op_params = {}
	op_fn = dic['operator'][0]

	if len(dic['operator']) > 1:
		op_params = dic['operator'][1]

	params = list(op_params.items()) + list({'source': source, 'target': target}.items())
	params = dict(params)
	output = {'operator': [op_fn, params]}
	return output


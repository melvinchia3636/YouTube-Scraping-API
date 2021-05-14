import inspect

def custom_property(f):
	def wrapper(self, *args, **kwargs):
		if not self.has_generated:
			self.parseData()
		return f(self, *args, **kwargs)
	return property(wrapper, doc=f.__doc__)
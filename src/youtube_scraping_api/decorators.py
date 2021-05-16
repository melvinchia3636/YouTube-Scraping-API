import inspect

def custom_property(f):
    def wrapper(self, *args, **kwargs):
        if self._is_builtin_callled and f.__name__ in self._static_properties:
            return self._static_properties[f.__name__]
        if not self._has_generated:
            self.parseData()
        return f(self, *args, **kwargs)
    return property(wrapper, doc=f.__doc__)
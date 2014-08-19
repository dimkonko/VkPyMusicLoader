import sys

class HandleForceExit(object):
	"""Check for errors
	This decorator checking if data is None and exit from
	program if there are any errors

	Returns:
		data - if no errors
		None - if have errors
	"""

	def __init__(self, func):
		self.func = func

	def __call__(self, text, isPassword=False):
		data = self.func(self.func, text, isPassword)
		if data is not None:
			return data
		else:
			sys.exit(1)
			return None
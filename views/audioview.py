import getpass

from decorators import HandleForceExit

class AudioView(object):
	def __init__(self):
		pass

	@HandleForceExit
	def get_input(self, text, isPassword=False):
		""" Handling a force exit in raw_input() func

		This function handling a force exit with 'ctrl + c' when taking input
		data with raw_input() function
		"""
		try:
			if isPassword:
				input_str = getpass.getpass(text)
			else:
				input_str = raw_input(text)

			return input_str
		except KeyboardInterrupt:
			print ""
			return None
	
	def login(self):
		user_data = dict()
		try:
			user_data["login"] = self.get_input("Login: ")
			user_data["password"] = self.get_input("Password: ", True)
		except KeyboardInterrupt:
			print ""
			return None

		return user_data

	def println(self, message):
		print message

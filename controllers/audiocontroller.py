import sys

from obj.song import Song

class AudioController(object):
	def __init__(self, app_id, model, view):
		"""
		Args:
			app_id - vk.com application id
			audio_model - audio model
			audio_view = audio_view
		"""
		self.app_id = app_id
		self.audio_model = model
		self.audio_view = view

	def _check_if_empty(self, data):
		"""Exit if @arg=data is empty
		This function checking if data is empty and
		exit from program if data is empty using
		@arg=exit as flag
		"""
		exit = False

		if isinstance(data, dict):
			for key in data:
				if not data[key]:
					exit = True
		else:
			if not data:
				exit = True

		if exit:
			self.audio_view.write("Exiting with empty data error...")
			sys.exit(0)

	def login(self):
		"""Login and get user data
		This function take login and password from
		input and trying to login on site vk.com.
		If login was successful we got a token and
		user_id
		else user_data will be empty
		"""
		login_data = self.audio_view.login()
		self._check_if_empty(login_data)

		login_data["app_id"] = self.app_id

		user_data = self.audio_model.login(login_data)

		if not user_data:
			self.audio_view.println("Wrong email or password")
			sys.exit(0)
		else:
			self.token = user_data["token"]
			self.user_id = user_data["user_id"]

	def init_song_list(self):
		"""Creating a list of Song object
		"""
		self.song_list = self._get_song_list()

	def process_comand(self, comand):
		try:
			if comand == 'q':
				return False
			elif ',' in comand:
				print ", in comand"
				comand = comand.replace(' ', '')
				songs_to_load = comand.split(',')

				for song_id in enumerate(songs_to_load):
					self.audio_model.load_and_save(self.song_list[int(song_id[1]) - 1])
			elif '-' in comand:
				comand = comand.split('-')
				start_sound = int(comand[0]) - 1
				end_sound = int(comand[1])
				for song_id_to_load in range(start_sound, end_sound):
					self.audio_model.load_and_save(self.song_list[song_id_to_load])
			else:
				song_id_to_load = int(comand) - 1

				if song_id_to_load < len(self.song_list) and song_id_to_load >= 0:
					self.audio_model.load_and_save(self.song_list[song_id_to_load])
				else:
					self.audio_view.println("This song doesn't exists")
		except:
		 	self.audio_view.println("Wrong comand")

	def get_input_comand(self):
		"""Gets comand from input
		"""
		return self.audio_view.get_input("Enter comand: ")

	def print_song_list(self):
		"""Printing song list
		"""
		for song in self.song_list:
			self.audio_view.println(str(song))

	def _get_song_list(self):
		"""Take a audio list from the server and
		return list with Song objects
		"""
		self.audio_view.println("Downloading playlist...")
		song_list = self.audio_model.get_song_list(self.token, self.user_id)
		returned_songs = list()
		counter = 1
		for song_dict in song_list:
			returned_songs.append(Song(counter, song_dict))
			counter += 1
		return returned_songs

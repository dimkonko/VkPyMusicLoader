import os

from controllers.audiocontroller import AudioController
from views.audioview import AudioView
from models.audiomodel import AudioModel

class VkMusicLoader(object):
	def __init__(self):
		self.controller = AudioController("4508332",
				AudioModel(os.path.dirname(os.path.realpath(__file__)) + "/Downloads/"),
				AudioView())
		self.controller.login()

	def start(self):
		self.controller.init_song_list()
		self.controller.print_song_list()

		while True:
			comand = self.controller.get_input_comand()
			if self.controller.process_comand(comand) is False:
				break


#Starting point
vk = VkMusicLoader()
vk.start()

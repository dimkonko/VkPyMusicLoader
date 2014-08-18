import json
import urllib2
import cookielib
import sys
import os
import getpass
from urllib import urlencode

from modules import vk_auth

from obj import song

class VkMusicLoader(object):
	def __init__(self, app_id,
			saving_directory=os.path.dirname(os.path.realpath(__file__)) + "/Downloads/"):

		buf_token_file = ".buf.txt"
		buf_token_file_dir = os.path.dirname(os.path.realpath(__file__)) + "/" + buf_token_file
		#os.remove(buf_token_file_dir)

		if not os.path.exists(buf_token_file_dir):
			try:
				email = raw_input("Login: ")
				password = getpass.getpass("Password: ")
			except:
				print ""
				sys.exit(0)
			try:
				self.token, self.user_id = vk_auth.auth(email, password, app_id, "audio")
			except:
				print "Wrong email or password"
				sys.exit(0)

			token_file = open(buf_token_file, "w")
			token_file.write(self.token)
			token_file.write("," + self.user_id)
			token_file.close()
		else:
			token_file = open(buf_token_file, "r")
			token_file_data = token_file.read().split(',')
			self.token = token_file_data[0]
			self.user_id = token_file_data[1]
			token_file.close()

		self.saving_directory = saving_directory

		if not os.path.exists(saving_directory):
			os.makedirs(saving_directory)

	def call_api(self, method, params, token):
	    params.append(("access_token", token))
	    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
	    return json.loads(urllib2.urlopen(url).read())["response"]

	def get_audio_list(self):
		self.returned_songs = list()
		self.songs = self.call_api("audio.get", [("uid", self.user_id)], self.token)
		self.counter = 1
		for song_dict in self.songs:
			self.returned_songs.append(song.Song(self.counter, song_dict))
			self.counter += 1
		return self.returned_songs

	def load_and_save(self, song):
		self.file_name = self.saving_directory + song.get_file_name() + ".mp3"

		if os.path.isfile(self.file_name):
			print "File " + self.file_name + " is already exists"
			return False

		self.u = urllib2.urlopen(song.url)
		self.f = open(self.file_name, 'wb')
		self.meta = self.u.info()
		self.file_size = int(self.meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (self.file_name, self.file_size)

		self.file_size_dl = 0
		self.block_sz = 8192
		while True:
		    buffer = self.u.read(self.block_sz)
		    if not buffer:
		        break

		    self.file_size_dl += len(buffer)
		    self.f.write(buffer)
		    self.status = r"%10d  [%3.2f%%]" % (self.file_size_dl, self.file_size_dl * 100. / self.file_size)
		    self.status = self.status + chr(8)*(len(self.status)+1)
		    print self.status,

		self.f.close()
		print "Success!"


print "This program using account from site: http://vk.com"

vk = VkMusicLoader("4508332")
songs = vk.get_audio_list()

for song in songs:
	print str(song)

while(True):
	try:
		input_songs = raw_input("Enter song(s) to load (Example: 20-30 or 11, 15): ")
	except:
		print ""
		sys,exit(1)

	try:
		if input_songs == 'q':
			break
		elif ',' in input_songs:
			input_songs = input_songs.replace(' ', '')
			songs_to_load = input_songs.split(',')

			for song_id in enumerate(songs_to_load):
				vk.load_and_save(songs[int(song_id[1]) - 1])
		elif '-' in input_songs:
			input_songs = input_songs.split('-')
			start_sound = int(input_songs[0]) - 1
			end_sound = int(input_songs[1])
			for song_id_to_load in range(start_sound, end_sound):
				vk.load_and_save(songs[song_id_to_load])
		else:
			song_id_to_load = int(input_songs) - 1

			if song_id_to_load < len(songs):
				vk.load_and_save(songs[song_id_to_load])
			else:
				print "This song doesn't exists"
				break
	except:
		print "Wrong comand"

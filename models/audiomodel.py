import json
import urllib2
import os
from urllib import urlencode

from modules import vk_auth

class AudioModel(object):
	def __init__(self, saving_directory):
		self.saving_directory = saving_directory

		if not os.path.exists(saving_directory):
			os.makedirs(saving_directory)

	def login(self, login_data):
		"""Authorize and return auth. data
		Returns:
			Dict - if login was successful
			None - if login failed
		"""
		try:
			token, user_id = vk_auth.auth(login_data["login"], login_data["password"],
									  	  login_data["app_id"], "audio")
			return {"token": token, "user_id": user_id}
		except :
			return None

	def _call_api(self, method, params, token):
	    params.append(("access_token", token))
	    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
	    return json.loads(urllib2.urlopen(url).read())["response"]

	def get_song_list(self, token, user_id):
		return self._call_api("audio.get", [("uid", user_id)], token)

	def load_and_save(self, song):
		file_name = self.saving_directory + song.get_file_name() + ".mp3"

		if os.path.isfile(file_name):
			print "File '" + song.get_file_name() + "' is already exists"
			return

		u = urllib2.urlopen(song.url)
		song_file = open(file_name, "wb")
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (file_name, file_size)

		file_size_dl = 0
		block_sz = 8192
		while True:
		    buffer = u.read(block_sz)
		    if not buffer:
		        break

		    file_size_dl += len(buffer)
		    song_file.write(buffer)
		    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		    status = status + chr(8)*(len(status)+1)
		    print status,

		song_file.close()
		print "Success!  "

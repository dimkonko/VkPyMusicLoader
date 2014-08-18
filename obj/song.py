#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

class Song(object):
	def __init__(self, song_id, song_dict):
		self.id = song_id
		self.artist = song_dict['artist']
		self.title = song_dict['title']
		self.duration = str(datetime.timedelta(seconds=int(song_dict['duration'])))
		self.url = song_dict['url']

	def get_file_name(self):
		returned_name = self.artist + ' - ' + self.title
		return returned_name.encode('utf-8')

	def __str__(self):
		return str(self.id) + ". " + self.get_file_name() + ", " + self.duration

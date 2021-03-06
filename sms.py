#!/usr/bin/python2.7
# -*- coding: utf8 -*-

import json
import os
import sys
import urllib

class FreeMobileSMS(object):

	def __init__(self, config=None):
		self._URL = "https://smsapi.free-mobile.fr/sendmsg?user={0}&pass={1}&msg={2}"
		self._codes = {
			200: "Message send",
			400: "Missing parameter",
			402: "Too much messages send",
			403: "Service not enable",
			500: "Server not available"
		}
		if config:
			with open(config, "r") as confFile:
				try:
					dataFile = json.load(confFile)
					self._login = dataFile["login"]
					self._token = dataFile["token"]
				except:
					raise Exception("Error with file " + self._file + "\n")
		else:
			if "SMS_LOGIN" not in os.environ:
				raise Exception("Missing SMS_LOGIN")
			if "SMS_TOKEN" not in os.environ:
				raise Exception("Missing SMS_TOKEN")
			self._login = os.environ["SMS_LOGIN"]
			self._token = os.environ["SMS_TOKEN"]

	def _makeRoute(self, message):
		return self._URL.format(self._login, self._token, urllib.quote(message))

	def _checkCode(self, code):
		if code in self._codes:
			return code, self._codes[code]
		else:
			return code, "Error message not found"

	def send(self, message):
		route = self._makeRoute(message)
		res = urllib.urlopen(route)
		return self._checkCode(int(res.getcode()))

def usage():
	print("Usage :")
	print("./sms.py [--config=file] message")

if __name__ == '__main__':
	if len(sys.argv) > 1 or not sys.stdin.isatty():
		config = None
		for arg in sys.argv:
			if arg.startswith("--config="):
				tab = arg.split("=")
				if (len(tab) > 1 and len(tab[1])):
					config = tab[1]
					sys.argv.remove(arg)
				else:
					usage()
					sys.exit(1)
		sms = FreeMobileSMS(config)
		if not sys.stdin.isatty():
			content = sys.stdin.read()
		else:
			content = sys.argv[1]
		code, message = sms.send(content)
		print (str(code) + " " + message)
	else:
		usage()
		sys.exit(1)

#!/usr/bin/python
import os, sys
from led_strip import LEDStrip

class LEDAnimation:
	def __init__(self, led_count=50, frame_count=100):
		self.led_strip_list = [ None ] * frame_count
		for n in range(0, frame_count):
			self.led_strip_list[n] = LEDStrip(led_count)

	# Setters and getters
	def get_frame_count(self):
		return len(self.led_strip_list)

	def get_frame(self, index=0):
		if index >= len(self.led_strip_list):
			return None

		return self.led_strip_list[index]

	# Animation functions
	def draw_animation(self, filename):
		for n in range(0, self.get_frame_count()):
			self.led_strip_list[n].draw_strip('data/strip_%04d.jpeg' % n)

		os.system('avconv -r 10 -i data/strip_%%04d.jpeg -b:v 1000k %s' % filename)
		os.system('rm data/strip*')

	# Debugging functions
	def __repr__(self):
		print 'LEDAnimation'

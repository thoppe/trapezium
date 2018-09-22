#!/usr/bin/python
import random, time

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

class LEDStrip:
	def __init__(self, led_count=50):
		self.led_count = led_count
		self.led_list = [[0xFF, 0xFF, 0xFF]] * self.led_count

		random.seed(time.time())
		for n in range(0, self.led_count):
			self.led_list[n] = [ random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) ]

	def draw_strip(self, filename):
		led_width = 20
		led_height = 20
		color_width = int(led_width*0.8)
		color_height = int(led_height*0.8)


		img = Image(width=(led_width*self.led_count), height=led_height, background=Color('#000000'))

		draw = Drawing()
		draw.stroke_width = 3

		for n in range(0, self.led_count):
			draw.fill_color = Color('#%02x%02x%02x' % (self.led_list[n][0], self.led_list[n][1], self.led_list[n][2]))
			draw.rectangle(left=int(led_width*n+0.5*(led_width-color_width)),
							top=int(0.5*(led_height-color_height)),
							width=color_width,
							height=color_height)
		draw(img)

		img.save(filename=filename)

	def __repr__(self):
		return 'LEDStrip'

#!/usr/bin/python
from led_strip import LEDStrip
from led_animation import LEDAnimation

#img = Image(format='jpeg', width=500, height=500, background=Color('#00FF00'))
#img.save(filename='output.jpeg')

#led_strip = LEDStrip(20)
#led_strip.draw_strip('output.jpeg')
#print(led_strip.led_list)

led_animation = LEDAnimation()
led_animation.draw_animation('data/test.mp4')

#for n in range(0, led_animation.get_frame_count()):
#	pass

	

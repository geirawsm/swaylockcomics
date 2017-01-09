#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
import os
from subprocess import Popen, PIPE,call, check_output
import PythonMagick
import re

from screeninfo import get_monitors
monitors = get_monitors()
monitor_w = re.search(r'monitor\((\d+)x\d+\+\d\+\d', str(monitors[0])).group(1)
monitor_h = re.search(r'monitor\(\d+x(\d+)\+\d\+\d', str(monitors[0])).group(1)

filedir = os.path.dirname(os.path.abspath(__file__))

#Hent dagens dato
now = pendulum.now().to_date_string()
# Hent nyeste Lunch-stripe
link = 'http://www.tu.no/tegneserier/lunch/?module=TekComics&service=image&id=lunch&key={}'.format(now)
stripe = '{}/striper/lunch-{}.jpg'.format(filedir, now)
tmp_lunch = '{}/temp_lunch.jpg'.format(filedir)
#Sjekk om siste fil allerede er henta
if not os.path.exists(stripe):
	if not os.path.exists('{}/striper'.format(filedir)):
		call(['mkdir','{}/striper'.format(filedir)])
	try:
		curl = call(['curl','-f',link,'-o',stripe])
		# Endre på størrelsen på bildet
		lunch = PythonMagick.Image(stripe)
		lunch.resize('150%')
		lunch.write(tmp_lunch)
	except:
		lunch = False
else:
	pass

tmp_out = '{}/out.png'.format(filedir)
call(['scrot','-z',tmp_out])

scrot = PythonMagick.Image(tmp_out)
scrot.scale('10%')
scrot.scale('1000%')
scrot.write(tmp_out)

tmp_lunch = '{}/temp_lunch.jpg'.format(filedir)
lunch = PythonMagick.Image(tmp_lunch)
lunch.font('/usr/share/fonts/TTF/LiberationSans-Bold.ttf')
lunch.annotate('github.com/armandg/i3lock-lunch', PythonMagick.GravityType.SouthEastGravity);
lunch_w = lunch.size().width()
lunch_h = lunch.size().height()
lunch_w = lunch_w // 2
lunch_h = lunch_h // 2
placement_w = (int(monitor_w) // 2)-lunch_w
placement_h = (int(monitor_h) // 2)-lunch_h
scrot.composite(lunch, placement_w, placement_h, PythonMagick.CompositeOperator.SrcOverCompositeOp)
scrot.write(tmp_out)

# Kjør lock-fil
call(['i3lock','-i',tmp_out])

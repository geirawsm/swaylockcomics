#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
import os
from subprocess import Popen, call
import PythonMagick
import re
import sys

from screeninfo import get_monitors
monitors = get_monitors()
monitor_w = re.search(r'monitor\((\d+)x\d+.*', str(monitors[0])).group(1)
monitor_h = re.search(r'monitor\(\d+x(\d+).*', str(monitors[0])).group(1)

serienavn = ['lunch', 'pondus']
serie = str(sys.argv[1])
if serie not in serienavn:
	print('Ingen seriestripe er definert. Kjør scriptet ved å for eksempel skrive \'python {} lunch\''.format(filename = os.path.basename(__file__)))
	sys.exit()

filedir = os.path.dirname(os.path.abspath(__file__))

# Hent nyeste stripe
if serie == 'lunch':
	now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
	link = 'http://www.tu.no/tegneserier/lunch/?module=TekComics&service=image&id=lunch&key={}'.format(now)
if serie == 'pondus':
	now = pendulum.now().format('DDMMYY', formatter='alternative')
	link = 'http://www.bt.no/external/cartoon/pondus/{}.gif'.format(now)

stripe = '{}/striper/{}-{}.jpg'.format(filedir, serie, now)
temp_stripe = '{}/temp_stripe.jpg'.format(filedir)
#Sjekk om siste fil allerede er henta
if not os.path.exists(stripe):
	if not os.path.exists('{}/striper'.format(filedir)):
		call(['mkdir','{}/striper'.format(filedir)])
	try:
		curl = call(['curl','-f',link,'-o',stripe])
		# Endre på størrelsen på bildet
		img = PythonMagick.Image(stripe)
		#img.resize('175%')
		img.resize('175%')
		img.write(temp_stripe)
	except:
		img = False
else:
	pass

temp_out = '{}/out.png'.format(filedir)
call(['scrot','-z',temp_out])

scrot = PythonMagick.Image(temp_out)
scrot.scale('10%')
scrot.scale('1000%')
scrot.write(temp_out)

img = PythonMagick.Image(temp_stripe)
img.font('/usr/share/fonts/TTF/LiberationSans-Bold.ttf')
img.annotate('github.com/armandg/i3lock-comics', PythonMagick.GravityType.SouthEastGravity);
img_w = img.size().width()
img_h = img.size().height()
img_w = img_w // 2
img_h = img_h // 2
placement_w = (int(monitor_w) // 2)-img_w
placement_h = (int(monitor_h) // 2)-img_h
scrot.composite(img, placement_w, placement_h, PythonMagick.CompositeOperator.SrcOverCompositeOp)
scrot.write(temp_out)

# Kjør lock-fil
call(['i3lock','-i',temp_out])

# Vedlikehold av mellomlagring av striper
temp_files = sorted(os.listdir('{}/striper'.format(filedir)))
# Sørg for at man ved sletting kun tar hensyn til bildene og ikke andre filer/mapper
for file in temp_files:
	if not '.jpg' in file:
		temp_files.remove(file)
# Behold kun de 5 nyeste stripene
if len(temp_files) > 5:
	clean_number = len(temp_files) - 5 - 1
	for i in temp_files[0:clean_number]:
		os.remove('{}/striper/{}'.format(filedir, i))
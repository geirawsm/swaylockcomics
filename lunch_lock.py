#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
import os
from subprocess import Popen, PIPE,call

filedir = os.path.dirname(os.path.abspath(__file__))

#Hent dagens dato
now = pendulum.now().to_date_string()
# Hent nyeste Lunch-stripe
link = 'http://www.tu.no/tegneserier/lunch/?module=TekComics&service=image&id=lunch&key={}'.format(now)
stripe = '{}/striper/lunch-{}.jpg'.format(filedir, now)
#Sjekk om siste fil allerede er henta
if not os.path.exists(stripe):
	if not os.path.exists('{}/striper'.format(filedir)):
		call(['mkdir','{}/striper'.format(filedir)])
	curl = call(['curl','-f',link,'-o',stripe])
	# Endre på størrelsen på bildet
	call(['convert',stripe,'-resize','150%','{}/temp_lunch.jpg'.format(filedir)])
else:
	pass
# Hvis 404, hva da?
tmp_file = '{}/tmp.jpg'.format(filedir)
call(['scrot','-z',tmp_file])
call(['convert',tmp_file,'-scale','10%','-scale','1000%',tmp_file])
call(['convert',tmp_file,'{}/temp_lunch.jpg'.format(filedir),'-gravity','center','-composite','{}/out.png'.format(filedir)])
# Kjør lock-fil
call(['i3lock','-i','{}/out.png'.format(filedir)])
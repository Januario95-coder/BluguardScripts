#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 18:31:43
"""

import os


os.chdir('C:/Users/hayysoft/Documents/APIs')
X = lambda s: os.system(s)
X('python manage.py runserver 0.0.0.0:5050')



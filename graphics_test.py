#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from drawille import Canvas
from math import sin, radians

c = Canvas()
for x in range(0, 3000, 10):
    c.set(x / 10, 10 + sin(radians(x)) * 10)

print(c.frame())
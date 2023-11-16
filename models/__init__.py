#!/usr/bin/python3
''' This module initializes a Storage instance and reloads data. '''

from models.engine.storage import Storage
strg = Storage()
strg.reload()

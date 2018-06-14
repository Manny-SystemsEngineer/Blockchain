#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:37:18 2018

@author: manny
"""
import hashlib

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256((str(self.index) +
                              str(self.timestamp) +
                              str(self.data) +
                              str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module containing the Block class
"""
import hashlib

class Block:
    """
    Class used to represent block within the blockchain

    :Inputs:
    index - the index of the block (normally incremented by the node)
    timestamp - the timestamp of when the block was created (normally handled by the node)
    data - the data contained within the block (for example: transactions, or documents)
    previous_hash - the hash of the previous block to provide integrity to the blockchain
    """
    def __init__(self, index, timestamp, data, previous_hash):
        """function used to initialise the block object"""
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """function which creates a hash of the block object"""
        sha = hashlib.sha256((str(self.index) +
                              str(self.timestamp) +
                              str(self.data) +
                              str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

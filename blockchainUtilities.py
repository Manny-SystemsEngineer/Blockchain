#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:42:33 2018

@author: manny
"""
from flask import request
import requests
import json
import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from blockClass import Block
from ast import literal_eval


def create_genesis_block():
    return Block(0, datetime.datetime.now(), {"proof-of-work": 9, "transactions": None}, "0")


def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = datetime.datetime.now()
    this_data = "Block ID:{0}".format(str(this_index))
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


def find_new_chains(peer_nodes):
    other_chains = []
    for node_url in peer_nodes:
        try:
            r = requests.get(node_url + "/blocks")
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"
        blocks = r.json()
        other_chains.append(blocks)
    return other_chains


def consensus(peer_nodes, blockchain):
    other_chains = find_new_chains(peer_nodes)
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain
    return blockchain

def signmessage(message, wallet_name):
    message =  bytes(message, encoding="UTF-8")
    hashed_message = SHA256.new(message)
    key_file = open(wallet_name+'_private_key.pem', 'rb')
    key = RSA.importKey(key_file.read())
    signature = pkcs1_15.new(key).sign(hashed_message)
    return hashed_message, signature

def verify_message(hashed_message, signature, wallet_name):
    if isinstance(wallet_name, str):
        key_file = open(wallet_name+'_public_key.pem', 'rb')
        public_key = RSA.importKey(key_file.read())
    else:
        public_key = wallet_name
    try:
        pkcs1_15.new(public_key).verify(hashed_message, signature)
        return True
    except (ValueError, TypeError):
        return False

def get_balance(wallet_name):
    if isinstance(wallet_name, str):
        key_file = open(wallet_name+'_public_key.pem', 'rb')
        public_key = RSA.importKey(key_file.read()).exportKey().decode("UTF-8")
    else:
        public_key = wallet_name.exportKey().decode("UTF-8")
    total = 0
    try:
        r = requests.get('http://localhost:5001/blocks')
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    blocks = r.json()
    #create list of unspent transactions
    for block in blocks:
        transactions = literal_eval(block['data'])['transactions']
        if transactions != None:
            for transaction in transactions:
                    if transaction['from'] == public_key:
                        total = total + float(-transaction['amount'])
                    if transaction['to'] == public_key:
                        total = total + float(transaction['amount'])
    return total

#blockchain = [create_genesis_block()]
#previous_block = blockchain[0]
#
#num_of_new_blocks = 10
#
# for i in range(0, num_of_new_blocks):
#    new_block = next_block(previous_block)
#    blockchain.append(new_block)
#    previous_block = new_block
#
#    print("Block #{0} has been added to the blockchain!".format(new_block.index))
#    print("Hash: {0}\n".format(new_block.hash))

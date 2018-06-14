#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:59:33 2018

@author: manny
"""
import json
import pickle
import datetime
from blockClass import Block
from blockchainUtilities import create_genesis_block, proof_of_work, consensus, verify_message, get_balance
from Crypto.PublicKey import RSA
from flask import Flask, request
node = Flask(__name__)

try:
    config = json.load(open('config.json'))
    node_wallet_name = config['node_settings']['node_wallet_name']
    mining = config['node_settings']['mining_enabled']
    node_ip_address = config['node_settings']['node_ip_address']
    node_port = config['node_settings']['node_port']
    peer_nodes = []
    for peer_node in config['peer_nodes']:
        peer_nodes.append(peer_node)
except:
    print("Error: Unable to load node config file")
    exit()


key_file = open(node_wallet_name+'_public_key.pem', 'rb')
node_addr= RSA.importKey(key_file.read()).exportKey().decode("UTF-8")


blockchain = []
if blockchain == []:
    try:
        blockchain = consensus(peer_nodes, blockchain)
    except:
        print("Can't connect to peer nodes")
if blockchain == []:
    print("No peer nodes found")
    try:
        with open('blockchain.pkl', 'rb') as blockchain_file:
            blockchain = pickle.load(blockchain_file)
        print("I'm pickle Chain! - blockchain initialised from local pkl file")
    except:
        print("No local blockchain found")
if blockchain == []:
    print("Generating local blockchain...")
    blockchain = [create_genesis_block()]

tmp_blockchain = blockchain


@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        if new_txion['amount'] < 0:
            return "Cannot process transactions of less than 0!\n", 403
        if new_txion['amount'] > get_balance(RSA.importKey(new_txion['from'].encode("UTF-8"))):
            return "Insufficient funds to carry out transaction!\n", 403
        else:
        #     verified = True
            #try:
            #    verified = verify_message(new_txion['hashed_message'], new_txion['signature'], RSA.importKey(new_txion['from'].encode("UTF-8")))
            #except (e):
            #    print(e)
            if verified != None:
                this_nodes_txions.append(new_txion)
                print("---New Transaction")
                print("FROM: {0}".format(new_txion['from']))
                print("TO: {0}".format(new_txion['to']))
                print("AMOUNT: #{0}".format(new_txion['amount']))
                print("VERIFIED: {0}".format(verified))
                return "Transaction submission successful!\n"
            else:
                return "Transaction not verified\n", 403


@node.route('/mine', methods=['GET'])
def mine():
    if mining == True:
        this_nodes_txions = []
        new_blockchain = consensus(peer_nodes, blockchain)
        last_block = new_blockchain[len(new_blockchain) - 1]
        last_proof = last_block.data['proof-of-work']
        proof = proof_of_work(last_proof)
        this_nodes_txions.append(
            {"from": "Mining", "to": node_addr, "amount": 1})
        new_block_data = {"proof-of-work": proof,
                          "transactions": list(this_nodes_txions)}
        new_block_index = last_block.index + 1
        new_block_timestamp = datetime.datetime.now()
        last_block_hash = last_block.hash
        this_nodes_txions[:] = []
        mined_block = Block(new_block_index,
                            new_block_timestamp,
                            new_block_data,
                            last_block_hash)
        new_blockchain.append(mined_block)
        store_blockchain()
        return json.dumps({"index": new_block_index,
                           "timestamp": str(new_block_timestamp),
                           "data": new_block_data,
                           "hash": last_block_hash}) + "\n"
    else:
        return "Mining not enabled!\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    new_blockchain = consensus(peer_nodes, blockchain)
    chain_to_send = []
    for block in new_blockchain:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = str(block.hash)
        new_block = {"index": block_index,
                     "timestamp": block_timestamp,
                     "data": block_data,
                     "hash": block_hash}
        chain_to_send.append(new_block)
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

def store_blockchain():
    new_blockchain = consensus(peer_nodes, blockchain)
    with open('blockchain.pkl', 'wb') as blockchain_file:
        pickle.dump(new_blockchain, blockchain_file, pickle.HIGHEST_PROTOCOL)


node.run(host=node_ip_address, port=int(node_port))

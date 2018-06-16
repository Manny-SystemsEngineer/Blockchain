#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 19:38:15 2018

@author: manny
"""
import json
import requests
from blockClass import Block
from blockchainUtilities import consensus
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from ast import literal_eval


def generate_key_pair(wallet_name):
    key = RSA.generate(1024)
    #export private key
    private_key = key.exportKey('PEM')
    file_out_private = open(wallet_name+'_private_key.pem', 'wb')
    file_out_private.write(private_key)
    file_out_private.close()

    public_key = key.publickey().exportKey('PEM')
    file_out_public = open(wallet_name+'_public_key.pem', 'wb')
    file_out_public.write(public_key)
    file_out_public.close()

def sign_message(message, wallet_name):
    message =  bytes(message, encoding="UTF-8")
    hashed_message = SHA256.new(message)
    key_file = open(wallet_name+'_private_key.pem', 'rb')
    key = RSA.importKey(key_file.read())
    signature = pkcs1_15.new(key).sign(hashed_message)
    return hashed_message, signature


def send_funds(wallet_name, recevier_wallet_name, amount, node="http://localhost:", port="5001"):
    key_file = open(wallet_name+'_public_key.pem', 'rb')
    public_key = RSA.importKey(key_file.read())
    if get_balance(public_key) < amount:
        print("Insufficient funds available for transfer")
    else:
        hashed_message, signature = sign_message(str(amount), wallet_name)
        recevier_key_file = key_file = open(recevier_wallet_name+'_public_key.pem', 'rb')
        recevier_key = RSA.importKey(key_file.read())
        transaction = {"from": public_key.exportKey().decode("UTF-8"),
                       "to": recevier_key.exportKey().decode("UTF-8"),
                       "amount": amount,
                       "hashed_message":  hashed_message.hexdigest(),
                       "signature": str(signature)}
        address = node + port
        r = requests.post(address + "/txion", json=transaction)
        if(r.status_code == 200):
            print("Transaction successful")
            mine_request = requests.get(address + "/mine")
        else:
            print(r)

#curl get_blocks to see all transactions
def get_balance(wallet_name):
    if type(wallet_name) == str:
        key_file = open(wallet_name+'_public_key.pem', 'rb')
        public_key = RSA.importKey(key_file.read()).exportKey().decode("UTF-8")
    else:
        public_key = wallet_name.exportKey().decode("UTF-8")
    total = 0
    r = requests.get('http://localhost:5001/blocks')
    blocks = r.json()
    #create list of unspent transactions
    for block in blocks:
        transactions = (literal_eval(block['data'])['transactions'])
        if transactions != None:
            for transaction in transactions:
                    if transaction['from'] == public_key:
                        total = total + float(-transaction['amount'])
                    if transaction['to'] == public_key:
                        total = total + float(transaction['amount'])
    return total

if __name__ =='__main__':
    pass
#send_funds("Other_Test_Wallet", "Test_Wallet", 100)
#print(get_balance("Other_Test_Wallet"))
#print(get_balance("Test_Wallet"))
#send_funds("Test_Wallet", "Other_Test_Wallet", 0)



#add values to create total
#when spent, add transaction to Used transactions list

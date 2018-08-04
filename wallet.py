#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 19:38:15 2018

@author: manny
"""
import json
import os
import requests
from blockClass import Block
from blockchainUtilities import consensus
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from ast import literal_eval


def generate_key_pair(wallet_name):
    key = RSA.generate(2048)
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
        key_file = open(recevier_wallet_name+'_public_key.pem', 'rb')
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
            requests.get(address + "/mine")
        else:
            print(r)

#curl get_blocks to see all transactions
def get_balance(wallet_name):
    if isinstance(wallet_name, str):
        key_file = open(wallet_name+'_public_key.pem', 'rb')
        public_key = RSA.importKey(key_file.read()).exportKey().decode("UTF-8")
    else:
        public_key = wallet_name.exportKey().decode("UTF-8")
    total = 0
    r = requests.get('http://localhost:5001/blocks')
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

def get_address_book(address_directory="./"):
    address_book = []
    for file in os.listdir(address_directory):
        if file.endswith(".pem"):
            if "public_key" in file:
                address_book.append(file.split("_public_key.pem")[0])
    print("--ADDRESS BOOK--")
    for address in address_book:
        print("{0} | {1} | {2}".format(address_book.index(address), address, get_balance(address)))
    return address_book





if __name__ =='__main__':
    #send_funds("Other_Test_Wallet", "Test_Wallet", 100)
    address_book = get_address_book()
    current_wallet = address_book[int(input("\nSelect a Wallet: ",))]
    print("\rLogged in as: {0}".format(current_wallet))
    address = address_book[int(input("Address to send to: ",))]
    amount = int(input("\rAmount to transfer to {0}: ".format(address),))
    send_funds(current_wallet, address, amount)
    print("\n")

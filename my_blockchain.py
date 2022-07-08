# Python program to create Blockchain

# For timestamp
import datetime
import json
from bitcoin import *
from hashlib import sha256
import time as t
# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain

class Blockchain:
    #This function is created to create the very first block and set its hash to "0"
    def __init__(self):
        self.prefix_zeros = 3
        self.prefix_str='0'*self.prefix_zeros
        self.chain = []
        self.create_block(previous_hash='0',transacciones = "")

    # This function is created to add further blocks into the chain
    def create_block(self, previous_hash, transacciones):
        data = {'index': len(self.chain) + 1,
                    'transacciones' : transacciones,
                    'timestamp': str(datetime.datetime.now()),
                    'previous_hash': previous_hash}
        final_block = self.proof_of_work(data, self.prefix_zeros)
        self.append_block(final_block)
        return final_block

    # This function check a new block
    def append_block(self,final_block):
        hash = self.hash256(final_block)
        if hash.startswith(self.prefix_str):
            self.chain.append(final_block)
        else:
            raise Exception("Bloque no válido")

    # This function is created to display the previous block
    def print_previous_block(self):
        return self.chain[-1]

    def hash256(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_chain(self):
        return self.chain

    # This is the function for proof of work and used to successfully mine the block
    def proof_of_work(self, block, prefix_zeros):
        begin=t.time()
        prefix_str='0'*prefix_zeros
        MAX_NONCE=10000000
        for nonce in range(MAX_NONCE):
            block['nonce'] = nonce
            hash = self.hash256(block)
            print(hash)
            if hash.startswith(prefix_str):
                print("Bitcoin mined with nonce value :",nonce)
                time_taken=t.time()- begin
                print("The mining process took ",time_taken,"seconds") 
                return block
        print("Could not find a hash in the given range of upto", MAX_NONCE)

    # def keys(self):
    #     #Generate private key
    #     my_private_key = random_key()
    #     #display private key
    #     print("Private Key: %sn" % my_private_key)
    #     #Generate public key
    #     my_public_key = privtopub(my_private_key)
    #     print("Public Key: %sn" % my_public_key)
    #     #Create a bitcoin address 
    #     my_bitcoin_address = pubtoaddr(my_public_key)
    #     print("Bitcoin Address: %sn" % my_bitcoin_address)

    # def chain_valid(self, chain):
    #     previous_block = chain[0]
    #     block_index = 1
    #     while block_index < len(chain):
    #         block = chain[block_index]
    #         if block['previous_hash'] != self.hash(previous_block):
    #             return False
    #         previous_proof = previous_block['proof']
    #         proof = block['proof']
    #         hash_operation = hashlib.sha256(
    #             str(proof**2 - previous_proof**2).encode()).hexdigest()
    #         if not hash_operation.startswith(self.prefix_str):
    #             return False
    #         previous_block = block
    #         block_index += 1
    #     return True
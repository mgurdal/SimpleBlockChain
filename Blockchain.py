from time import time
import hashlib
import json
import requests
from urllib.parse import urlparse


class Blockchain(object):
    """
        Yazarlar: Merve Hanımefendi
    """
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(address)
        print(self.nodes)

    def PoW(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = "{}{}".format(last_proof, proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" # False


    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]# 2.
            print('{last_block}'.format(last_block=last_block))
            print('{block}'.format(block=block))
            print("\n-----------\n")

            # block hashlerini kontrol et
            if block['previous_hash'] != self.hash(last_block):
                return False

            # pow doğru mu kontrol et
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index +=1
        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        print(self.nodes)
        for node in neighbours:# localhost:5000
            resp = requests.get(node) #

            if resp.status_code == 200:

                chain_data = resp.json()
                length = chain_data['length']
                chain = chain_data['chain']
                print(chain)
                if length > max_length and self.valid_chain(chain):
                    max_length = length
            else:
                raise Exception("No!")

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
        'sender': sender,
        'recipient': recipient,
        'amount': amount
        })
        print("{} {} {} gönderdi.".format(
            sender, recipient, amount
        ))
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string =  json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

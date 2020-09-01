# blockchain.py - Blockchain Class
import hashlib
from time import time
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """ This method will contain two parameters proof, previous hash """
        block = {
            'index': len(self.chain) + 1,
            'timestamp' : time(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions=[]
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """ This will create a new transaction which will be sent to the next
        block. It will contain three variables including sender, recipient and
        amount """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """ The follow code will create a SHA-256 block hash and also ensure
        that the dictionary is ordered """

        block_string = json.dumps(block).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ Calls and returns the last block of the chain """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """ This method is where you the consensus algorithm is implemented.
        It takes two parameters including self and last_proof """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """ This method validates the block """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def blockchainTest():
    bc = Blockchain()
    bc.new_transaction("Billy", "Jane", "3 BTC")
    bc.new_transaction("Jane", "Billy", "2.5 BTC")
    print(bc.current_transactions)
    bc.new_block(666)
    bc.new_transaction("Jane", "Ruk", "1 BTC")
    bc.new_transaction("Ruk", "Billy", "1 BTC")
    bc.new_transaction("Billy", "Luke", "3.5 BTC")
    print(bc.current_transactions)
    bc.new_block(7890)

    print(bc.chain)

if __name__ == '__main__':
    blockchainTest()

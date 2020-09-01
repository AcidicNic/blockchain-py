# app.py - Flask Server
from flask import Flask, jsonify, request
from blockchain import Blockchain
from uuid import uuid4
import json

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    """Here we make the proof of work algorithm work"""
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': 'The new block has been forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash' : block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient', values['amount']])
    response = {'message': f'Transaction is scheduled to be added to Block No. {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : str(len(blockchain.chain)),
    }
    return jsonify(chain=blockchain.chain, length=len(blockchain.chain))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

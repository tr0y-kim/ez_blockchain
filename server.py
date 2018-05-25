from flask import Flask
import flask
import json
from textwrap import dedent
from uuid import uuid4

# Our blockchain.py API
from blockchain import Blockchain

# /transactions/new : to create a new transaction to a block
# /mine : to tell our server to mine a new block.
# /chain : to return the full Blockchain.

app = Flask(__name__)
# Universial Unique Identifier
node_identifier = str(uuid4()).replace('-','')

blockchain = Blockchain()

@app.route('/mine',methods=['GET'])
def mine():
	return "Mine a new Block!!"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return 'missing values', 400
	index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
	response = {'message' : 'Transaction will be added to Block {0}'.format(index)}
	
	return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
		'chain' : blockchain.chain,
		'length': len(blockchain.chain),
	}

	return jsonify(response), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)

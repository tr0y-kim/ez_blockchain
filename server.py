from flask import Flask, request, jsonify
import json
from time import time
from textwrap import dedent
from uuid import uuid4

# Our blockchain.py API
from blockchain import Blockchain

# /transactions/new : to create a new transaction to a block
# /mine : to tell our server to mine a new block.
# /chain : to return the full Blockchain.
# /nodes/register : to accept a list of new nodes in the form of URLs
# /nodes/resolve : to implement our Consensus Algorithm

app = Flask(__name__)
# Universial Unique Identifier
node_identifier = str(uuid4()).replace('-','')

blockchain = Blockchain()

@app.route('/mine',methods=['GET'])
def mine():
	last_block = blockchain.last_block
	last_proof = last_block['proof']

	proof = blockchain.pow(last_proof)
	# print "DEBUGGING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	blockchain.new_transaction(
			sender='0',
			recipient=node_identifier,
			amount=1 # coinbase transaction
	)
	# Forge the new Block by adding it to the chain
	previous_hash = blockchain.hash(last_block) # ??????????
	block = blockchain.new_block(proof, previous_hash)

	response = {
		'message' : 'new block found',
		'index' : block['index'],
		'transactions' : block['transactions'],
		'proof' : block['proof'],
		'previous_hash' : block['previous_hash']
	}

	return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return 'missing values', 400
	
	# Create a new Transaction
	index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
	response = {'message' : 'Transaction will be added to Block {%s}' % index}
	
	return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
		'chain' : blockchain.chain,
		'length': len(blockchain.chain),
	}

	return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
	values = request.get_json()

	nodes = values.get('nodes')
	if nodes is None: # Bad Request 400
		return "Error: Please supply a valid list of nodes", 400

	for node in nodes:
		blockchain.register_node(node)

	response = {
		'message' : 'New nodes have been added',
		'total_nodes': list(blockchain.nodes),
	}
	return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
	replaced = blockchain.resolve_conflicts() # True False return

	if replaced:
		response = {
			'message' : 'Our chain was replaced',
			'new_chain' : blockchain.chain
		}
	else:
		response = {
			'message' : 'Our chain is authoritative',
			'chain' : blockchain.chain
		}
	return jsonify(response), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)

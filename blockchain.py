import hashlib
import json
from time import time

####### block generation & its principle

class Blockchain(object):
	# initialize the blockchain info
	def __init__(self):
		self.chain = []
		self.current_transaction = []
		# genesis block
		self.new_block(previous_hash=1, proof=100)

	def new_block(self,proof,previous_hash=None):
		block = {
			'index': len(self.chain)+1,
			'timestamp': time(), # timestamp from 1970
			'transactions': self.current_transaction,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1])
		}
		self.current_transaction = []
		self.chain.append(block)
		return block

	def new_transaction(self,sender,recipient,amount):
		self.current_transaction.append(
			{
				'sender' : sender,
				'recipient' : recipient,
				'amount' : amount				
				
			}
		)
		return self.last_block['index'] + 1

	# directly access from class, share! not individual instance use it
	@staticmethod
	def hash(block):
		block_string = json.dumps(block, sort_keys=True).encode()
	
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		return self.chain[-1]

	def pow(self, last_proof):
		proof = 0
		while self.valid_proof(last_proof, proof) is False:
			proof += 1

		return proof

	@staticmethod
	def valid_proof(last_proof, proof):
		guess = str(last_proof + proof).encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000" # nonce

'''
Project: Blockchain based Electronic Voting Machine (EVM)
Author : Ketan Verma
Date   : 23 December 2017

Description: This is a demo concept before actually building a fully working
application. The purpose of this demo is to brainstorm ideas and get a sense of
what all problems could arise in building such a project.
'''

from random import randint
from blockchain import Blockchain
from result import Result

# Create some constants
block_size           = 20
genesis_block_secret = 'This is the secret. Keep it safe!'
nb_votes_to_generate = 200

# Create an instance of this class
blockchain = Blockchain(block_size, genesis_block_secret)

# Add some dummy votes and get a summary of the blockchain
for i in range(nb_votes_to_generate):
    blockchain.new_vote(randint(1, 5))
blockchain.summary()

# Create an instance of the result class that will verify the votes and calculate the result
result = Result(blockchain, block_size, genesis_block_secret)
voting_result = result.verify_integrity()

if voting_result[0] == Result.RESULT_OK:
    print("The results are not tampered!")
    print(voting_result[1])
else:
    print("Failed to verify integrity of the blockchain")
    print("Tampered Block: " + str(voting_result[1]))
    print("Found Hash    : " + voting_result[2])
    print("Expected Hash : " + voting_result[3])

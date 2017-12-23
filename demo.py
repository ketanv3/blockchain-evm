'''
Project: Blockchain based Electronic Voting Machine (EVM)
Author : Ketan Verma
Date   : 23 December 2017

Description: This is a demo concept before actually building a fully working
application. The purpose of this demo is to brainstorm ideas and get a sense of
what all problems could arise in building such a project.
'''

from hashlib import sha256
from collections import deque
from time import time
from random import randint

class Block():
    # Some constants and return codes
    ERROR_BLOCK_FULL    = -1
    TRANSACTION_SUCCESS =  0

    # Set the parameters for the Block
    def __init__(self, block_id, block_size, starting_hash):
        self.block_id      = block_id
        self.starting_hash = starting_hash
        self.ending_hash   = starting_hash
        self.block_size    = block_size
        self.block         = deque()
        print("Adding a new Block on the Blockchain: " + str(block_id))

    # Function to create a vote transaction on the block
    # vote_for is the index of the party for which the vote is created
    def new_vote(self, vote_for):
        # Make sure that the current block is not full.
        # In case the block is already full, return the error so that the
        # new vote can be added to a new block altogether.
        if len(self.block) >= self.block_size:
            return Block.ERROR_BLOCK_FULL

        # The current block is not full, we add a new vote to it
        # Create a new transaction on the block
        transaction = {
            'vote_for': vote_for,
            'timestamp': time()
        }
        transaction_hash = '::'.join([str(self.block_id), str(self.block_size), str(transaction['vote_for']), str(transaction['timestamp']), str(self.ending_hash)])
        transaction_hash = sha256(transaction_hash.encode('utf-8')).hexdigest()
        transaction['hash'] = transaction_hash

        # Append the new transaction to the block and update the ending hash
        self.block.append(transaction)
        ending_hash = transaction_hash
        return Block.TRANSACTION_SUCCESS

    # Function to get the ending hash of the block
    def get_ending_hash(self):
        return self.ending_hash


class Blockchain():
    # Set the parameters for the blockchain
    def __init__(self, block_size, genesis_block_secret):
        self.block_size         = block_size
        self.genesis_block_hash = sha256(genesis_block_secret.encode('utf-8')).hexdigest()

        # Create the blockchain and the first block on it
        self.blockchain = deque()
        self.blockchain.append(Block(0, self.block_size, self.genesis_block_hash))

    # Function to return the starting hash for the blockchain
    def get_genesis_block_hash(self):
        return self.genesis_block_hash

    # Function to create a vote transaction on the blockchain
    # We first try to perform the transaction on the current block,
    # if it fails being full, we create a new block on the blockchain append
    # add the new transaction to the newly created block.
    def new_vote(self, vote_for):
        # We will try to add the new transaction on the last block on the blockchain
        # If the current_block is already full, then we create a new block and add a transaction to it
        current_block = self.blockchain[-1]
        if len(current_block.block) >= self.block_size:
            self.blockchain.append(Block(len(self.blockchain), self.block_size, current_block.get_ending_hash()))
            current_block = self.blockchain[-1]

        # We are now sure that the current_block does have space for a new transaction
        transaction_status = current_block.new_vote(vote_for)

    # Function to summarise the blockchain
    def summary(self, only_hashes = True):
        for block in self.blockchain:
            print("\nBlock: " + str(block.block_id))
            t = 0
            for transaction in block.block:
                print("   " + str(t) + ": " + transaction['hash'])
                if not only_hashes:
                    print("      vote_for: " + str(transaction['vote_for']) + "   timestamp: " + str(transaction['timestamp']))
                t += 1


# Create an instance of this class
blockchain = Blockchain(block_size = 50, genesis_block_secret = 'This is the secret. Keep it safe!')

# Add some dummy votes and get a summary of the blockchain
for i in range(500):
    blockchain.new_vote(randint(1, 5))
blockchain.summary()


# TODO: Create another class that verifies the integrity of these transactions
# and calculates the final result of the elections.

from collections import deque
from hashlib import sha256
from time import time

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
        self.ending_hash = transaction_hash
        return Block.TRANSACTION_SUCCESS

    # Function to get the ending hash of the block
    def get_ending_hash(self):
        return self.ending_hash

from block import Block
from hashlib import sha256
from collections import deque

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

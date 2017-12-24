from collections import deque
from hashlib import sha256
from blockchain import Blockchain
from block import Block

class Result():
    INTEGRITY_CHECK_FAILED = -1
    RESULT_OK              =  0

    # Set the parameters that will be used to verify the integrity of the blockchain
    def __init__(self, blockchain, block_size, genesis_block_secret):
        self.blockchain         = blockchain
        self.block_size         = block_size
        self.genesis_block_hash = sha256(genesis_block_secret.encode('utf-8')).hexdigest()

    # Create a function that verifies the integrity of the blockchain
    def verify_integrity(self):
        # This will keep the track of voting results
        result_count = {}

        # Initialise the previous hash with the value of genesis_block_hash
        previous_hash = self.genesis_block_hash

        # This will track the time of the last transaction
        # This will make sure that transactions are in non-decreasing order of
        # time; which makes it harder to tamper with.
        previous_transaction_time = 0

        # Outer loop that runs over all the blocks in a blockchain
        for block in self.blockchain.blockchain:
            # Inner loop that runs over all the transactions in the current block
            for transaction in block.block:
                # This should be the expected hash for the current transaction
                expected_hash = '::'.join([str(block.block_id), str(block.block_size), str(transaction['vote_for']), str(transaction['timestamp']), str(previous_hash)])
                expected_hash = sha256(expected_hash.encode('utf-8')).hexdigest()

                # Compare the expected_hash with the actual hash stored in the transaction
                found_hash = transaction['hash']

                if expected_hash != found_hash:
                    # The hashes don't match. There is an integrity error in this
                    # or the previous transaction
                    return Result.INTEGRITY_CHECK_FAILED, block.block_id, found_hash, expected_hash

                # The hashes match, update the result counter, previous_hash
                # and move to the next transaction
                result_count[transaction['vote_for']] = result_count.get(transaction['vote_for'], 0) + 1
                previous_hash = expected_hash

        # No tampered transaction found
        return Result.RESULT_OK, result_count

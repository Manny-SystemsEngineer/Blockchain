import unittest
import sys
sys.path.append("..")
import blockchainUtilities

class nodeTest(unittest.TestCase):
    """Class to hold the unit tests for the node module"""
    def setUp(self):
        """Method to set up the test environment"""
        self.gensis_block = blockchainUtilities.create_genesis_block()

    def test_create_genesis_block(self):
        """Method to test that the gensis block is correctly created"""
        self.assertEqual(self.gensis_block.index, 0, msg="Gensis block index incorrectly set")

    def test_next_block(self):
        """Method to test that the next block is correctly created"""
        self.new_block = blockchainUtilities.next_block(self.gensis_block)
        self.assertEqual(self.new_block.index, 1, msg="Next block index incorrectly set")

    def test_proof_of_work(self):
        """Method to test that proof of work is correctly calculated"""
        self.proof = blockchainUtilities.proof_of_work(9)
        self.assertEqual(self.proof, 18, msg="Proof of work incorrectly calculated")

if __name__ == '__main__':
    unittest.main()
    
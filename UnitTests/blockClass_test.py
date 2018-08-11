import unittest
import sys
from blockClass import Block

class blockClassTest(unittest.TestCase):
    """Class to hold the unit tests for the Block Class"""
    def setUp(self):
        """Method to set up the test environment"""
        self.test_block = Block(1, "0:0:0", "test_data", 0)

    def test_block_index(self):
        """Method to test that the block index is correctly set"""
        self.assertEqual(self.test_block.index, 1, msg="Block index incorrectly set")

    def test_block_timestamp(self):
        """Method to test that the block timestamp is correctly set"""
        self.assertEqual(self.test_block.timestamp, "0:0:0", msg="Block timestamp incorrectly set")

    def test_block_data(self):
        """Method to test that the block data is correctly set"""
        self.assertEqual(self.test_block.data, "test_data", msg="Block data incorrectly set")

    def test_block_previous_hash(self):
        """Method to test that the previous block's hash is correctly set"""
        self.assertEqual(self.test_block.previous_hash, 0, msg="Block previous hash incorrectly set")

    def test_block_hash(self):
        """Method to test that the block is able to correctly hash itself"""
        self.assertEqual(self.test_block.hash, '26a798ea9981d68f1573a8b4e0b2c89ee9338b12a5ac48833485487d6bad04f7', msg="Block self hash incorrect")


if __name__ == '__main__':
    unittest.main()
    
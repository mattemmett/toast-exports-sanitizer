import unittest
import os
import file_handler

class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_output"
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_create_output_directory(self):
        self.assertFalse(os.path.exists(self.test_dir))
        file_handler.create_output_directory(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))

if __name__ == "__main__":
    unittest.main()

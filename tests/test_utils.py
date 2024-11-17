import unittest
import utils

class TestUtils(unittest.TestCase):

    def test_load_environment_variables(self):
        # Create a temporary .env file for testing
        env_file = ".env.test"
        with open(env_file, "w") as f:
            f.write("TEST_KEY=TEST_VALUE\n")

        # Load the environment variables from the temporary .env file
        utils.load_environment_variables(env_file)

        # Check if the environment variable is loaded correctly
        self.assertEqual(os.getenv("TEST_KEY"), "TEST_VALUE")

        # Clean up the temporary .env file
        os.remove(env_file)

if __name__ == "__main__":
    unittest.main()

import os

def create_output_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

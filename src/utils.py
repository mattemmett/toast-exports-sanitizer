import os
import json

def load_environment_variables(env_file=".env"):
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    else:
        raise FileNotFoundError(f"{env_file} not found")

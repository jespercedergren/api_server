import os

project_dir = os.path.dirname(os.path.abspath(__file__))

try:
    test_env = os.environ["test_env"]
except KeyError as e:
    test_env = "local"

import os
import flask

def get_env_var(var_name):
    return os.environ.get(var_name)
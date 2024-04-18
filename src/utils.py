# utils.py

import os

def create_db_path(name, base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(base_dir, name)
    full_path = "sqlite:///" + db_path
    if not os.path.isdir(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    return full_path


def list_public_attributes(obj):
    # Filter out magic methods and sort
    attributes = [attr for attr in dir(obj) if not attr.startswith('__')]
    attributes.sort()  # Sorting the attributes for better readability
    return attributes


def print_public_attributes(obj):
    attributes = list_public_attributes(obj)
    for idx, attr in enumerate(attributes, start=1):
        print(f"{idx}: {attr}")


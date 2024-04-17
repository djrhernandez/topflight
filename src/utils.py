# utils.py

import os

def create_db_path(name):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    return "sqlite:///" + os.path.join(BASE_DIR, name)
    

def prettify_dir(obj):
    # Filter out magic methods and sort
    attributes = [attr for attr in dir(obj) if not attr.startswith('__')]
    attributes.sort()  # Sorting the attributes for better readability

    obj = []
    # Printing the attributes in a more readable format
    for idx, attr in enumerate(attributes, start=1):
        print(f"{idx}: {attr}")
        obj.append((idx, attr))
        
    return obj
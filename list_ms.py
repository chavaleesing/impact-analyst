import os

def list_folders_in_path(path):
    # List all folders in the specified path
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

path = '../repo/processor'
folders = list_folders_in_path(path)
# print(folders)
for f in folders:
    print(f)

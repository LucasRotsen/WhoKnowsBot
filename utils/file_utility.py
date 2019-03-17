import os


def append(path: str, content: str):
    file = open(path, 'a')
    file.write(content)
    file.close()


def read(path: str):
    file = open(path, 'r')
    content = file.read()
    file.close()
    return content


def write(path: str, content: str):
    file = open(path, 'w')
    file.write(str(content))
    file.close()


def delete_file(path: str):
    os.remove(path)


def check_and_create_folder(path: str):
    try:
        os.makedirs(path)
    except FileExistsError:
        # directory already exists
        pass

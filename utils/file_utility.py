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

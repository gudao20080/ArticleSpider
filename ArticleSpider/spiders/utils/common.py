import hashlib

def get_md5(url: str):
    m = hashlib.md5()
    m.update()
    return m.hexdigest()
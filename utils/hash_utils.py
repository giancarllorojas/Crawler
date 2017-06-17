import hashlib

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYXZ-_"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def hash_url(url):
    url_hashed= int(hashlib.sha256(url.encode('utf-8')).hexdigest(), 16) % 10**15
    return baseN(url_hashed, 64)
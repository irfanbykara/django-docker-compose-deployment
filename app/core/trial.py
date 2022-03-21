import hashlib


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
hash_string = '18Evler!'
sha_signature = encrypt_string(hash_string)
print(sha_signature)


my_list = []

my_dict = {'hello':1,
           'hello2':2,
           'hello3':3,
           'hello4':4}

print(my_dict.values())
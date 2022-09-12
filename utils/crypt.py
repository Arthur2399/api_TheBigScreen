import cryptocode
def encrypt(word):
    str_encoded = cryptocode.encrypt(word,"TheBigScreen")
    return str_encoded

## And then to decode it:
def decrypt(word):
    str_decoded = cryptocode.decrypt(word, "TheBigScreen")
    return str_decoded
def alphabet_index_sub(prev: str, i: int):
    if i >= 26:
        return alphabet_index_sub(chr((i%26)+65) + prev, i//26-1)
    return chr(i + 65) + prev
    
def alphabet_index(index: int):
    return alphabet_index_sub("", index)
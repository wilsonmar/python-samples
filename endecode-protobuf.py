#!/usr/bin/env python3

""" endecode-protobuf.py at https://github.com/wilsonmar/python-samples/blob/main/endecode-protobuf.py
STATUS: Kinda working - not putting # between commas in rawlist.
"v002 rm self but commas ignored :endecode-protobuf.py"

Encode and decode a list of strings like Protobuf for gRPC by 
prefixing each string with a count delimited by # character.
From Neetcode at https://youtube.com/shorts/zwUjHW8Exyc?si=zJqvmNgYht_Oajwq
"This is a common interview question".
"""

    # NOTE:  Python requires self to be explicitly defined as the first parameter in instance methods.
    # Use self to clearly distinguish between instance variables and local variables within methods.
def encode(strs: list[str]) -> str:
    res = ""
    for s in strs:
        res += str(len(s)) + "#" + s
    return res


def decode(s:str) -> list[str]:
    res = []
    i = 0

    while i < len(s):
        j = 1
        while s[j] != "#":
            j += 1
        length = int(s[i:j])
        i = j + 1
        j = i + length
        res.append(s[i:j])
        i = j

    return res


def main():

    rawlist = ["I, love, you"]

    # NOTE: Can't separate using # because the string can contain that separation character.
    #print(f"*** rawlist={rawlist}")

    encoded = encode(rawlist)
    print(f"*** enecoded={encoded}")

    decoded = decode(encoded)
    print(f"*** decoded={decoded}")


if __name__ == "__main__":
    main()

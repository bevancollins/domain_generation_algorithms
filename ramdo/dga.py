import argparse

def dga(seed, nr):
    s = (2 * seed * (nr + 1))
    r = s ^ (26 * seed * nr)
    domain = ""
    for i in xrange(16):
        r = r & 0xFFFFFFFF
        domain += chr(r % 26 + ord('a'))
        r += (r ^ (s*i**2*26))
 
    domain += ".org"
    return domain

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nr", type=int, default=20, help="number of domains")
args = parser.parse_args()

for nr in range(args.nr):
    print(dga(0xD5FFF, nr))



import hashlib
from datetime import datetime, timedelta
import argparse


def dga(date, key, nr):

    for index in range(nr):
        seed = 8*[0]
        seed[0] = ((date.year & 0xFF) + 0x30) & 0xFF
        seed[1] = date.month & 0xFF
        seed[2] = date.day & 0xFF
        seed[3] = 0
        r = (index) & 0xFFFFFFFE
        for i in range(4):
            seed[4+i] = r & 0xFF
            r >>= 8

        seed_str = ""
        for i in range(8):
            k = (key >> (8*(i%4))) & 0xFF if key else 0
            seed_str += chr((seed[i] ^ k))

        m = hashlib.md5()
        m.update(seed_str)
        md5 = m.digest()

        domain = ""
        for m in md5:
            tmp = (ord(m) & 0xF) + (ord(m) >> 4) + ord('a')
            if tmp <= ord('z'):
                domain += chr(tmp)

        tlds = [".biz", ".info", ".org", ".net", ".com"]
        for i, tld in enumerate(tlds): 
            m = len(tlds) - i
            if not index % m: 
                domain += tld
                break


        print(domain)

if __name__=="__main__":
    # known keys:
    # -k D6D7A4BE
    # -k DEADC2DE
    # -k D6D7A4B1
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-k", "--key", help="key", default=None)
    parser.add_argument("-n", "--nr", type=int, default=1020, help="number of domains")
    args = parser.parse_args()
    if args.key:
        key = int(args.key, 16)
    else:
        key = None
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    dga(d, key, args.nr)

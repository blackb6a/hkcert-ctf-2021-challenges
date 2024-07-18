import hashlib
import string
import itertools
import re
alphabet = string.digits + string.ascii_letters
word='hkcert';

i=1;
while True:
    print("Current Value of i: "+ str(i));
    for password in itertools.product(alphabet, repeat=i):
        temp= ''.join(password)
        #print(temp)
        hash=hashlib.md5((word+temp).encode('utf-8')).hexdigest();
        if ((hash[:2]=='0e' and hash[2:].isdecimal()) or (hash[:3]=='00e' and hash[3:].isdecimal())):
            print((word+temp)+": "+hash)
    i+=1;
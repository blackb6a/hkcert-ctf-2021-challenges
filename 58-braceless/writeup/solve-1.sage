# https://facthacks.cr.yp.to/batchgcd.html
from tqdm import tqdm
from datetime import datetime
import time

def log(msg, important=False):
    t = datetime.fromtimestamp(time.time())
    print(f'[{"*" if important else " "}] {t} | {msg}')

def producttree(X):
    result = [X]
    while len(X) > 1:
        log(f'Start computing product tree: {len(X)}')
        X = [prod(X[i*2:(i+1)*2]) for i in range((len(X)+1)//2)]
        result.append(X)
        log(f'Finish computing product tree: {len(X)}')
    return result

def batchgcd_faster(X):
    prods = producttree(X)
    R = prods.pop()
    while prods:
        X = prods.pop()
        log(f'Start computing remainder tree: {len(X)}')
        R = [R[floor(i//2)] % X[i]**2 for i in range(len(X))]
        log(f'Finish computing remainder tree: {len(X)}')
    return [gcd(r//n,n) for r,n in zip(R,X)]

with open('transcript.log') as f:
    lines = f.readlines()

ns = []
for i in tqdm(range(15000)):
    n = gcd(
        2^65537 - int(lines[7*i+4], 16),
        3^65537 - int(lines[7*i+6], 16),
    )
    ns.append(int(n))

t1 = time.time()
gcds = batchgcd_faster(ns)
t2 = time.time()
log(f'Time elapsed: {t2-t1}s')

for i, g in enumerate(gcds):
    if g < 1000: continue
    n = ns[i]
    log('Small factor:')
    log(f'-> n = {ns[i]}', important=True)
    log(f'-> g = {g}', important=True)
    log(f'-> encrypted_secret = {int(lines[7*i+8], 16)}', important=True)

'''
Experiment:
4096 1024-bit numbers: 66.42s
8192 1024-bit numbers: 272.30s
'''
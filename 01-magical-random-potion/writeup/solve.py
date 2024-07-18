from pwn import *
from tqdm import tqdm
import base64

class Challenge:
    def __init__(self):
        self.r = remote('chalp.hkcert21.pwnable.hk', 28201)
        self.attempts = 0

    def mul(self, u, v):
        self.attempts += 1
        u, v = [base64.b64encode(x).decode() for x in [u, v]]
        u, v = [x + '='*(88-len(x)) for x in [u, v]]
        self.r.sendlineafter('> ', f'MUL {u} {v}')
        return base64.b64decode(self.r.recvline().decode().strip())

    def pow(self, u, v):
        self.attempts += 1
        u, v = [base64.b64encode(x).decode() for x in [u, v]]
        u, v = [x + '='*(88-len(x)) for x in [u, v]]
        self.r.sendlineafter('> ', f'POW {u} {v}')
        return base64.b64decode(self.r.recvline().decode().strip())

    def and_(self, u, v):
        self.attempts += 1
        u, v = [base64.b64encode(x).decode() for x in [u, v]]
        u, v = [x + '='*(88-len(x)) for x in [u, v]]
        self.r.sendlineafter('> ', f'AND {u} {v}')
        return base64.b64decode(self.r.recvline().decode().strip())

    def or_(self, u, v):
        self.attempts += 1
        u, v = [base64.b64encode(x).decode() for x in [u, v]]
        u, v = [x + '='*(88-len(x)) for x in [u, v]]
        self.r.sendlineafter('> ', f'OR {u} {v}')
        return base64.b64decode(self.r.recvline().decode().strip())

    def attempt(self, u):
        self.attempts += 1
        self.r.sendlineafter('> ', f'ATTEMPT {u}')
        return self.r.recvline().decode().strip()

    def get_secret(self):
        self.attempts += 1
        self.r.sendlineafter('> ', f'SECRET')
        return base64.b64decode(self.r.recvline().decode().strip())

    def send_raw(self, raw):
        self.r.sendlineafter('> ', raw)
        return base64.b64decode(self.r.recvline().decode().strip())

    def end(self):
        self.r.close()

# s = 2^128 - 2
def make_s(challenge, one):
    while True:
        s = os.urandom(16)
        s = challenge.or_(s, s)
        if challenge.or_(s, one) != s: break
    for _ in range(15):
        while True:
            s2 = os.urandom(16)
            s2 = challenge.or_(s2, s2)
            if challenge.or_(s2, one) != s2: break
        s = challenge.or_(s, s2)
    return s

# randomly return a power of two
def get_power_of_two(challenge, s, zero):
    t1 = s[:]

    recent_ten = list(range(15))
    while len(set(recent_ten)) > 2:
        r = os.urandom(16)
        t2 = challenge.and_(t1, r)
        recent_ten = recent_ten[1:] + [t2]

        if t2 == zero: continue
        t1 = t2
    return t1
        

def solve1():
    cnt = 0
    while True:
        cnt += 1
        print(f'[ ] Trying for the {cnt}-th time')

        challenge = Challenge()
        encrypted_secret = challenge.get_secret()

        zero = challenge.and_(b'', b'')
        one = challenge.pow(zero, zero)
        s = make_s(challenge, one) # 2^128 - 2

        four = challenge.mul(s, s)
        four = challenge.and_(four, s)

        # Probability of passing: 1 - (127/128)^n
        n = 80
        for _ in range(n):
            two = get_power_of_two(challenge, s, zero)
            if challenge.pow(two, two) == four: break
        else:
            print(f'[ ] No good! Tried {challenge.attempts} times.')
            challenge.end()
            continue
        print(f'[*] Cool! Let\'s proceed. Tried {challenge.attempts} times.')

        powers_of_two = [one, two]
        for _ in tqdm(range(2, 512)):
            powers_of_two.append(challenge.mul(powers_of_two[-1], two))

        # Recover p
        p, ep = 1, zero
        for i in tqdm(range(511, 0, -1)):
            ep2 = challenge.or_(ep, powers_of_two[i])
            if challenge.and_(ep2, one) == one: continue
            ep = ep2
            p += (1<<i)
        print(f'[*] Recovered p = {hex(p)}')

        # Recover the secret
        mixed = 0
        for i in tqdm(range(512)):
            if challenge.and_(encrypted_secret, powers_of_two[i]) != zero:
                mixed |= (1<<i)
        
        secret = mixed ^ p
        print(f'[*] Recovered secret = {hex(secret)}')

        flag = challenge.attempt(secret)
        print(f'[*] Flag = {flag}')
        print(f'[*] Tried {challenge.attempts} times.')
        return

# Can we reduce the number of calls (or available functions)?
# or make it more cryptographic-related?

solve1() # ~45% chance to success each time. ~3.5k calls
'''
    harrier — 2021/05/03
    i have Enc(0), Enc(1)
    so Enc(a & 1) == Enc(a) -> is_odd
    now generate random Enc(x) such that all x is even
    then do the same thing for 0, i get a decreasing sequence in number of 1's, and ultimately 0
    with large enough trial and with prob i think this can get 2?

    Mystiz ✔✔ — 2021/05/03
    how you get enc(1)

    harrier — 2021/05/03
    0^0?

    Mystiz ✔✔ — 2021/05/03
    ok
    How you get a decreasing sequence

    harrier — 2021/05/03
    But that's hard, even with decreasing sequence cant sure it's 2, it can be 2^i :(

    Mystiz ✔✔ — 2021/05/03
    right
    and how you ensure it is 2^i instead of 2^i+2^j

    harrier — 2021/05/03
    We have inclusion, ie a | b == a implies a > b and number of ones of a > b
    So we can help strict decreasing chains and possibly combine chains
    But testing between few smallest in different decreasing chain can be computational intensive :/

    Mystiz ✔✔ — 2021/05/03
    actually this makes sense
    since i have not limit the number of oracle calls, i will agree this as a valid algorithm

    harrier — 2021/05/03
    With limit number of Oracle calls even  getting 0 from that could be difficult :cold_face:
    Oh. So target is to construct 256 size 1 number with this then kill
'''


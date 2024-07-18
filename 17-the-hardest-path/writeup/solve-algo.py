from tqdm import tqdm
import sys

sys.setrecursionlimit(2000)

with open('chall.py') as f:
    lines = f.readlines()

lines = lines[16:-11]

exists = {}
for line in lines:
    if line.endswith('_29aa7a86665899ed\n'): continue
    u, v = line.split(' = ')
    v = v.split('"')[1::2]

    exists[u] = u

mp = {}
for line in lines:
    if line.endswith('_29aa7a86665899ed\n'): continue
    u, v = line.split(' = ')
    v = v.split('"')[1::2]

    v = [exists.get(x) for x in v]
    mp[u] = v

nm = [[0 for _ in range(201)] for _ in range(201)]
def fill(n, x, y):
    if nm[x][y]: return
    nm[x][y] = 1
    for n2, (dx, dy) in zip(mp[n], [(-1, 0), (0, 1), (0, -1), (1, 0)]):
        if n2 is None: continue
        fill(n2, x+dx, y+dy)

fill('_328518a497015157', 1, 1)

n = 100
maze = nm
def dijkstra(x1, y1, x2, y2):
    queue = [(x1, y1)]
    distances = [[0x3f3f3f3f for _ in range(2*n+1)] for _ in range(2*n+1)]
    distances[x1][y1] = 0
    while len(queue) > 0 and distances[x2][y2] == 0x3f3f3f3f:
        x, y = queue.pop(0)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if maze[x+dx][y+dy] == 0: continue
            if distances[x+dx][y+dy] < 0x3f3f3f3f: continue

            queue.append((x+dx, y+dy))
            distances[x+dx][y+dy] = distances[x][y]+1
    
    if distances[x2][y2] == 0x3f3f3f3f:
        return None
    return distances

ds = dijkstra(199, 199, 1, 1)

path = ''
x, y = 1, 1
while x != 199 or y != 199:
    for dx, dy, u in [(-1, 0, 'N'), (0, 1, 'E'), (0, -1, 'W'), (1, 0, 'S')]:
        if ds[x][y] != ds[x+dx][y+dy]+1: continue
        x += dx
        y += dy
        path += u
        break
    print(x, y, path, len(path))

# SSSSEENNEESSSSEENNEEEEEEEESSSSEESSSSWWSSSSEESSEESSSSWWSSSSWWWWWWSSWWSSSSSSEEEESSSSEESSEESSSSSSSSEENNEESSEEEESSEESSSSEESSEEEEEEEESSEEEESSSSEEEEEENNNNNNEENNWWNNEEEENNNNEEEENNEEEEEESSSSWWSSWWSSSSEEEESSWWSSEESSEEEESSSSEENNNNNNEEEESSEESSEESSEEEESSEENNEENNWWNNEEEEEESSEEEEEENNNNWWWWNNWWNNNNWWNNEEEEEENNEENNWWWWNNWWNNEENNEEEEEEEESSEESSEESSSSEESSEEEEEENNEESSSSSSEEEEEENNNNNNNNNNNNNNNNEEEEEEEEEEEESSEESSSSWWWWSSSSSSWWSSEESSEEEEEENNNNEESSEESSEEEENNEENNNNEEEEEENNEENNWWWWWWNNNNWWSSSSWWSSSSWWWWNNNNNNNNNNEENNEENNEENNEEEESSEESSSSEEEEEESSEEEEEEEENNNNEENNNNWWNNEEEENNNNEEEEEESSSSSSSSSSSSSSSSSSSSSSEESSSSEEEEEESSEESSWWSSSSEESSSSEEEENNEEEESSWWSSSSSSSSWWSSWWWWWWSSWWWWSSWWNNNNWWWWWWSSEESSWWSSWWSSEESSSSSSSSSSWWSSEEEESSSSSSEEEESSSSEESSEESSSSEEEESSEENNEEEESSSSWWSSEESSWWSSSSWWWWNNWWSSSSEESSEEEESSWWSSSSWWWWNNWWNNWWSSSSWWWWWWWWWWWWWWSSSSSSWWWWSSEESSWWSSWWWWWWSSWWWWWWWWSSSSEESSEEEEEESSSSSSEEEESSSSEEEEEESSWWWWSSSSSSSSSSSSEEEEEESSEEEENNEEEENNEEEENNEEEENNEEEESSEENNEEEESSSSSSSSWWSSWWSSSSWWSSSSSSEESSSSEEEESSEENNEESSEEEE

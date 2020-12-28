#!/usr/bin/python3
from collections import defaultdict
from hashlib import md5
from itertools import combinations, product
from copy import deepcopy

lines = open("day24.dat").read().splitlines()

E = dict()

def dist(f,t):

  def getNei(p, dist):
    ret = dict()
    tocheck = [(p[0]+1,p[1]),(p[0]-1,p[1]),
      (p[0],p[1]+1), (p[0],p[1]-1)]
    #print("tocheck", tocheck, "for", p)
    for tc in tocheck:
      #print(tc, lines[tc[1]][tc[0]])
      if lines[tc[1]][tc[0]] == ".":
        ret[tc] = dist+1

    return ret

  D = dict()
  D[f] = 0
  N = getNei(f,D[f])

  while t not in D:
    #print(N)
    pos = min(N, key=N.get)

    if pos not in D:
      D[pos] = N[pos]
      nei = getNei(pos, N[pos])
      #print(N, "neis", nei)
      N.update(nei)
      #print(N)
    elif (pos in D) & (D[pos] > N[pos]):
      D[pos] = N[pos]
      getNei(pos, N[pos])
      #print(N, "neis", nei)
      N.update(nei)
    else:
      pass

    N.pop(pos)

  return D[t]

def minDist(f, visited, part2 = False):
  tovisit = []
  for k in E.keys():
    if k not in visited:
      tovisit.append(k)

  dist = 10000
  if len(tovisit) == 0:
    if part2 == True:
      dist = DL[(f,0)]
    else:
      dist = 0
  for tv in tovisit:
    myvisited = visited[:]
    myvisited.append(tv)
    tmp = minDist(tv, myvisited, part2)
    tmp += DL[(f, tv)]
    dist = min(tmp, dist)

  return dist
  

for y,v in enumerate(lines):
  lines[y] = [x for x in v]
  for x,v in enumerate(lines[y]):
    if v in [str(x) for x in range(10)]:
      E[int(v)] = (x,y)

for k,v in E.items():
  lines[v[1]][v[0]] = "."

DL = dict()

for k1,v1 in E.items():
  for k2,v2 in E.items():
    if k1 == k2:
      continue
    if (k1,k2) not in DL.keys():
      DL[(k1,k2)] = dist(E[k1], E[k2])
      DL[(k2,k1)] = DL[k1,k2]


print("Part1:", minDist(0, [0]))
print("Part2:", minDist(0, [0], True))



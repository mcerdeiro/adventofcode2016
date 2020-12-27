#!/usr/bin/python3
from hashlib import md5
from collections import deque
from copy import deepcopy

lines = open("day22.dat").read().splitlines()

G = dict()
X = 0
Y = 0

def getNei(pos):
  ret = []
  tocheck = [(pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)]
  for tc in tocheck:
    if tc in G.keys():
      ret.append(tc)

  return ret

def markWalls():
  global X,Y
  for k in G.keys():
    X = max(X, k[0]+1)
    Y = max(Y, k[1]+1)
  for k,v in G.items():
    G[k]["d"] = False
    if k == (X-1,0):
      G[k]["d"] = True
    nks = getNei(k)

    wall = True
    partialwall = 0
    for nk in nks:
      if v["u"] < 94:
        wall = False
      if v["u"] <= G[nk]["s"]:
        partialwall += 1
    if partialwall == len(nks):
      v["p"] = False
    else:
      v["p"] = True
    if wall == True:
      v["w"] = True
    else:
      v["w"] = False
    
def printNodes():
  for y in range(Y):
    tmp = ""
    for x in range(X):
      if G[(x,y)]["d"] == True:
        tmp += "D "
      elif G[(x,y)]["u"] == 0:
        tmp +="E "
      elif G[(x,y)]["w"] == True:
        tmp += "| "
      elif G[(x,y)]["p"] == True:
        tmp += "P "
      else:
        tmp += ". "
    print(tmp)


def moveE(pose):
  cpose = None
  for k,v in G.items():
    if G[k]["u"] == 0:
      cpose = k
      break

  last = None
  found = False
  for y in range(Y):
    for x in range(X):
      if G[(x,y)]["w"] != True:
        last = (x,y)
      else:
        found = True
        break
    if found:
      break

  movements = abs(cpose[0]-last[0]) + abs(cpose[1]-last[1])
  movements += abs(pose[0]-last[0]) + abs(pose[1]-last[1])

  return movements

def part2():
  markWalls()
  posd = (X-1,0)
  pose = (posd[0]-1, 0)
  movements = moveE(pose)
  movements += 1
  posd, pose = pose, posd

  movements += posd[0] * 5
  return movements

def process(line):
  #/dev/grid/node-x0-y0     85T   72T    13T   84%
  y = int(line.split()[0].split("-")[-1][1::])
  x = int(line.split()[0].split("-")[-2][1::])
  size = int(line.split()[1][0:-1])
  used = int(line.split()[2][0:-1])
  global G
  G[(x,y)] = {"s": size, "u": used}

for line in lines:
  if line.startswith("root"):
    pass
  elif line.startswith("Filesystem"):
    pass
  else:
    process(line)

ans1 = 0
for k1,v1 in G.items():
  for k2, v2 in G.items():
    if k1 == k2:
      continue
    if v1["u"] > 0:
      if v1["u"] <= v2["s"] - v2["u"]:
        ans1 += 1

print("Part1:", ans1)
print("Part2:", part2())
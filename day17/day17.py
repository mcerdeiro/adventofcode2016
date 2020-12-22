#!/usr/bin/python3
from hashlib import md5

inp = "veumntbg"

def checkDoors(msg, pos):
  hash = md5(msg.encode("UTF")).hexdigest()[0:4]
  open = ["b", "c", "d", "e", "f"]
  doors = ["U", "D", "L", "R"]
  status = dict()

  for i in range(len(hash)):
    if hash[i] in open:
      status[doors[i]] = "O"
    else:
      status[doors[i]] = "C"

  if pos[1] == 0:
    status["U"] = "C"
  if pos[1] == 3:
    status["D"] = "C"
    
  if pos[0] == 0:
    status["L"] = "C"
  if pos[0] == 3:
    status["R"] = "C"

  return status

def solve(msg, pos, part1 = True):
  if pos == (3,3):
    return msg
  options = checkDoors(msg, pos)
  results = []
  for k,v in options.items():
    #print(msg, options, "checking", k, v)
    #input()
    if v == "O":
      mypos = (pos[0]+{"U": 0, "D": 0, "L":-1, "R":1}[k], \
               pos[1]+{"U": -1, "D": 1, "L":0, "R":0}[k])
      ret = solve(msg+k, mypos, part1)
      if ret != None:
        results.append(ret)

  if len(results) == 0:
    return None
  
  results = sorted(results, key=lambda x: len(x))

  if part1:
    return results[0]
  else:
    return results[-1]

ret = solve(inp, (0,0))
print(ret[len(inp)::])

ret = solve(inp, (0,0), False)
print(len(ret)-len(inp))
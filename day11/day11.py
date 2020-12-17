#!/usr/bin/python3
from collections import defaultdict
from hashlib import md5
from itertools import combinations, product
from copy import deepcopy

lines = open("day11.dat").read().splitlines()

data = {}
floorstr = {"first": 1, "second": 2, "third": 3, "fourth": 4}

def isValidFloor(data, floor):
  #only chips is ok
  #only generator is ok
  #if a chip is with a generator it has also it owns generator
  chips = []
  generators = []
  for el in data:
    if el[1] == "G":
      generators.append(el)
    elif el[1] == "M":
      chips.append(el)
    else:
      assert(0)

  if len(generators) == 0:
    return True
  else:
    if len(chips) == 0:
      return True
    else:
      for chip in chips:
        if (chip[0]+"G") not in generators:
          return False
  return True

def isValidConfig(data):
  for k,v in data.items():
    if k not in ["E", "dist"]:
      if not isValidFloor(v, k):
        return False

  return True

def printData(data):
  print("*** ***                   dist:", data["dist"])
  print("                          val:", getValue(data))
  allel = []
  for k,v in data.items():
    if k not in ["E", "dist"]:
      allel += v
  allel = sorted(allel)


  for i in range(4,0,-1):
    toprint = "" 
    toprint += "F"+str(i)+" "

    if data["E"] == i:
      toprint += " E  "
    else:
      toprint += " .  "
    for el in allel:
      if el in data[i]:
          toprint += el + "  "
      else:
        toprint += ".   "

    print(toprint)

def process_input(line):
  floor = None
  val = []

  floor = floorstr[line.split(" floor contains ")[0].split()[-1]]
  if line.count("nothing relevant") == 0:
    contains = line.split("floor contains ")[1][0:-1].replace("and ", "").replace("a ","").split(", ")
    for con in contains:
      letters = ""
      for word in con.upper().split():
        letters += word[0]
      val.append(letters)

  return floor, val

for line in lines:
  f, v = process_input(line)
  data[f] = v
data["E"] = 1
data["dist"] = 0

def getCombinations(elements):
  comb2 = []
  comb1 = []
  for i in range(1, min(len(elements)+1,3)):
    if i == 2:
      comb2 += list(combinations(elements, i))
    elif i == 1:
      comb1 += list(combinations(elements, i))

    else:
      assert(0)

  #print(comb)
  return comb2, comb1

def isEnd(data):
  for i in range(1,4):
    if len(data[i]) != 0:
      return True

  return False

def isElementDown(data):
  for i in range(data["E"]-1,0,-1):
    if len(data[i]) != 0:
      return True
  return False

def possibleNextSteps(data):
  options = []
  
  comb2, comb1 = getCombinations(data[data["E"]])
  newlevels = []
  
  if data["E"] < 4:
    newlevels.append(data["E"]+1)  
  if data["E"] > 1:
    if (isElementDown(data)):
      newlevels.append(data["E"]-1)

  comb = comb1 + comb2
  optionsup1 = []
  optionsup2 = []
  optionsdown1 = []
  optionsdown2 = []

  for nl in newlevels:
    for co in comb:
      tmp = deepcopy(data)
      for c in co:
        tmp[tmp["E"]].remove(c)
      tmp["E"] = nl
      for c in co:
        tmp[tmp["E"]].append(c)
      tmp["dist"] += 1
    
      if (isValidConfig(tmp)):
        if nl > data["E"]:
          if len(co) == 1:
            optionsup1.append(tmp)
          else:
            optionsup2.append(tmp)
        else:
          if len(co) == 1:
            optionsdown1.append(tmp)
          else:
            optionsdown2.append(tmp)

    if len(optionsup2) > 0:
      options += optionsup2
    else:
      options += optionsup1
    if len(optionsdown1) > 0:
      options += optionsdown1
    else:
      options += optionsdown2
    
  
  # if len(options) == 0:
  #   printData(data)
  #   print("comb1", comb1, "comb2", comb2)
  # assert(len(options) > 1)
  return options

# the hieher the value the near to goal
def getValue(data):
  val = 0
  elements = 0
  for i in range(1,5,+1):
    val = len(data[i])*i
    elements += len(data[i])

  goal = elements * 4

  val = data["dist"] // 2 * elements // 8 - val
  #val = goal - val

  return val

def compWODistWOEqual(data1, data2):
  states1 = {}
  for k,v in data1.items():
    if k in ["E"]:
      if v != data2["E"]:
        return False
    elif k in ["dist"]:
      # ignore distance to compare
      pass
    else:
      for el in v:
          states1[el] = k

  states2 = {}
  for k,v in data2.items():
    if k in ["E"]:
      pass
    elif k in ["dist"]:
      # ignore distance to compare
      pass
    else:
      for el in v:
          states2[el] = k

  statespairs1 = []
  for k,v in states1.items():
    if k[1] == "G":
      statespairs1.append((v, states1[k[0]+"M"]))

  statespairs2 = []
  for k,v in states2.items():
    if k[1] == "G":
      statespairs2.append((v, states2[k[0]+"M"]))

  for state in statespairs1:
      if state in statespairs2:
        if statespairs1.count(state) == statespairs2.count(state):
          pass
        else:
          return False
      else:
        return False

  return True  

assert(compWODistWOEqual(
    {"E": 3, 1: [], 2: [], 3: ["HG", "LG", "HM", "LM"], 4: [], "dist": 7},
    {"E": 3, 1: [], 2: [], 3: ["HG", "LG", "HM", "LM"], 4: [], "dist": 7}
) == True)
assert(compWODistWOEqual(
    {"E": 3, 1: ["HG", "HM"], 2: [], 3: ["LG", "LM"], 4: [], "dist": 7},
    {"E": 3, 1: ["LG", "LM"], 2: [], 3: ["HG", "HM"], 4: [], "dist": 7},
) == True)


def compWODist(data1, data2):
  for k,v in data1.items():
    if k in ["E"]:
      if v != data2[k]:
        return False
    elif k in ["dist"]:
      pass
    else:
      for e in v:
        if e not in data2[k]:
          return False

  return True

def comp(data1, data2):
  for k,v in data1.items():
      if k in ["E", "dist"]:
        if v != data2[k]:
          return False
      else:
        for e in v:
          if e not in data2[k]:
            return False

  return True

debug = False
def solve(start):
  options = [start]
  history = []

  while isEnd(options[0]):
    #print("Dist", options[0]["dist"])
    if debug:
      print("using")
      printData(options[0])

    history.append(options[0])
    opt = possibleNextSteps(options.pop(0))
    for o1 in opt:
      found = False
      for o2 in options:
        if compWODistWOEqual(o1, o2):
          found = True
          break
      for o2 in history:
        if compWODistWOEqual(o1, o2):
          found = True
          break

      if found == False:
        #if getValue(o1) > getValue(history[-1]):
          options.append(o1)
        # else:
        #   print("Discarting")
        #   printData(o1)
        #   print("since old is better")
        #   printData(history[-1])

    #options = sorted(options, key=lambda x: x["dist"])
    options = sorted(options, key=getValue)

    if debug:  
      print("new turn")
      for o in options:
        printData(o)
  #    pass

  printData(options[0])

print("Part1")
solve(data)
print("Part2")
data[1] += ["EG", "EM", "DG","DM"]
solve(data)


# Tests
assert(isValidFloor(["HM", "LM"],0) == True)
assert(isValidFloor(["HG"],0) == True)
assert(isValidFloor(["LG"],0) == True)
assert(isValidFloor(["LG", "HM", "LM"],0) == False)
assert(isValidFloor(["HG", "LG", "HM", "LM"],0) == True)

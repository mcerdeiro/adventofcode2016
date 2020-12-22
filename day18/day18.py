#!/usr/bin/python3
from hashlib import md5

line = open("day18.dat").read().splitlines()[0]

def getNextLine(last):
  newline = ""
  for i in range(len(last)):
    c = line[i]
    l = "."
    r = "."
    if i < len(last)-1:
      r = last[i+1]
    if i > 0:
      l = last[i-1]

    new = "."
    if (l == c == "^") & (r != "^"):
      new = "^"
    if (c == r == "^") & (l != "^"):
      new = "^"
    if (r == c == ".") & (l == "^"):
      new = "^"
    if (l == c == ".") & (r == "^"):
      new = "^"
    newline += new

  return newline

ans1 = 0
for i in range(40):
  ans1 += line.count(".")
  #print("Line", line)
  line = getNextLine(line)
  
print("Part1", ans1)

ans2 = ans1
for i in range(400000-40):
  ans2 += line.count(".")
  line = getNextLine(line)
  
print("Part2", ans2)

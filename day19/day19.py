#!/usr/bin/python3
from hashlib import md5

inp = 3017957

def part1(inp):
  n = 3
  while n < inp:
    last = n
    n = n*2+1
  
  return abs(last-inp)*2-1

def part2(inp):
  n = 3
  while n < inp:
    last = n
    n = n * 3

  if inp < last*2:
    return -last+inp
  else:
    return inp*2-last

print("Part1:", part1(inp))
print("Part2:", part2(inp))

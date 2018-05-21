#!/usr/bin/env python3

import ipaddress
import sys

prefixes = set()

for prefix in sys.stdin:
  try:
    prefixes.add(ipaddress.ip_network(prefix.rstrip('\n')))
  except ValueError:
    print(prefix.rstrip('\n'))

def find_supernet(subnet):
  # find supernets
  for prefix in range(1,subnet.prefixlen+1):
    if subnet.supernet(prefixlen_diff=prefix) in prefixes:
      if subnet in prefixes: prefixes.remove(subnet)
      return

def find_neighbors(subnet):
  # find neighbors
  neighbors = list(subnet.supernet(prefixlen_diff=1).subnets())
  if neighbors[0] in prefixes:
    if neighbors[1] in prefixes:
      prefixes.remove(neighbors[0])
      prefixes.remove(neighbors[1])
      if subnet.supernet(prefixlen_diff=1) not in prefixes: prefixes.add(subnet.supernet(prefixlen_diff=1))
      find_neighbors(subnet.supernet(prefixlen_diff=1))

def merge(subnet):
  if subnet in prefixes:
    find_supernet(subnet)
    find_neighbors(subnet)

old_prefixes = prefixes.copy()
for subnet in old_prefixes:
  merge(subnet)

for prefix in prefixes:
  print(prefix)

#!/usr/bin/env python

from __future__ import print_function
import argparse
import numpy as np

parser = argparse.ArgumentParser(
  description='                                                        \
Generates a set of nodes, elements, and surfaces given an              \
input of intervals or an array.                                        \
                                                                       \
At least one of -x or -y must be supplied, otherwise failure.          \
If only one is passed, then other will be assumed to be of             \
same structure.                                                        \
')

fhelp='read nodes from file'
xfhelp='read x nodes from file'
yfhelp='read y nodes from file'
xhelp='1st column linspace(a,b,n)'
yhelp='2nd column linspace(a,b,n)'
bhelp='Boundary conditions for bottom, right, top, and left wall'

bdef = [
  'temp-bottom-wall',
  'temp-right-wall ',
  'temp-top-wall   ',
  'temp-left-wall  ',
]

parser.add_argument(
  '--file','-f',type=str,help=fhelp,default=None,metavar='xyz-file'
)
parser.add_argument(
  '--xfile',type=str,help=xfhelp,default=None,metavar='x.txt'
)
parser.add_argument(
  '--yfile',type=str,help=yfhelp,default=None,metavar='y.txt'
)
parser.add_argument(
  '-x',type=float,help=xhelp,default=None,metavar='a b N',nargs=3
)
parser.add_argument(
  '-y',type=float,help=yhelp,default=None,metavar='a b N',nargs=3
)
parser.add_argument(
  '--boundary','-b',
  type=str,help=bhelp,default=bdef,metavar='b r t l',nargs=4
)

args = parser.parse_args()

if args.file:
  x,y = np.loadtxt(args.file).T
elif args.xfile or args.yfile:
  if args.xfile:
    x = np.loadtxt(args.xfile).T
  if args.yfile:
    y = np.loadtxt(args.yfile).T
  if args.xfile and not args.yfile:
    y = x.copy()
  elif args.yfile and not args.xfile:
    x = y.copy()
else:
  if args.x:
    x = np.linspace(args.x[0],args.x[1],int(args.x[2]))
  if args.y:
    y = np.linspace(args.y[0],args.y[1],int(args.y[2]))
  if args.x and not args.y:
    y = x.copy()
  elif args.y and not args.x:
    x = y.copy()

m,n          = len(x),len(y)
num_nodes    = m*n
num_elements = (m-1)*(n-1)
num_surfaces = 2*( m + n - 2 )

print('<NODES NUMBER={:d}>'.format(num_nodes))
c = 1 
for k in y: 
  for j in x:
    out   = [c,j,k,0.]
    s_out = '  {:>4d}\t{:> 5.3f}\t{:> 5.3f}\t{:> 5.3f}'.format(*out)
    print(s_out)
    c += 1
print('</NODES>\n')

print('<ELEMENTS NUMBER={:d}>'.format(num_elements))
c = 1 
for k in range(n-1):
  base_row = k * m
  for j in range(m-1):
    base_col = j+1
    jk       = base_row + base_col
    elements = [jk, jk+1, jk+1+m, jk+m]
    s_out    = '  {:>4d} <Q>  '.format(c)
    s_out   += (4*'{:>4d}    ').format(*elements)
    s_out   += '</Q>'
    print(s_out)
    c += 1
print('</ELEMENTS>\n')

print('<SURFACES NUMBER={:d}>'.format(num_surfaces))
c = 1
N = n-1
M = m-1
for edge in range(1,5):
  if edge == 1:
    elems     = [ j for j in range(1,m) ]
    temp_type = args.boundary[0]
  elif edge == 2:
    elems = [ M*k for k in range(1,n) ]
    temp_type = args.boundary[1]
  elif edge == 3:
    elems = [ num_elements - j for j in range(M) ]
    temp_type = args.boundary[2]
  elif edge == 4:
    elems = [ M*(N - k) + 1 for k in range(1,n) ]
    temp_type = args.boundary[3]
  for e in elems:
    out = [c, e, edge ]
    s_out  = '  ' + (3*'{:>4d}  ').format(*out)
    s_out += '<B> {:s} </B>'.format(temp_type)
    print(s_out)
    c += 1
print('</SURFACES>')



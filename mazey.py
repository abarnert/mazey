#!/usr/bin/env python3

from collections import namedtuple
from enum import Enum, auto

MAZE = """
 . . . . 
. . . . .
 @ . E . 
. F U S .
 I L K . 
. B S E .
 . A E . 
. . . S .
 Z Y E . 
. M C N .
 A N E . 
. A E O .
 D U . . 
. Q Z O .
 . . . . 
. . . . .
""".splitlines()[1:]

class Dir(Enum):
    N = 0
    NE = 1
    SE = 2
    S = 3
    SW = 4
    NW = 5
    def rotate(self, n):
        return Dir((self.value + n) % len(Dir))
    def left(self):
        return self.rotate(-1)
    def right(self):
        return self.rotate(1)
N, NE, SE, S, SW, NW = Dir.N, Dir.NE, Dir.SE, Dir.S, Dir.SW, Dir.NW

Pos = namedtuple('Pos', 'x y dir'.split())

class Board:
    def __getitem__(self, xy):
        x, y, *_ = xy
        ltr = MAZE[y][x]
        if ltr == ' ':
            raise IndexError(f'{x}, {y} not a hex position')
        return ltr
    def neighbor(self, pos, dir):
        x, y, *_ = pos
        if dir == N:
            return Pos(x, y-2, dir)
        elif dir == NE:
            return Pos(x+1, y-1, dir)
        elif dir == SE:
            return Pos(x+1, y+1, dir)
        elif dir == S:
            return Pos(x, y+2, dir)
        elif dir == SW:
            return Pos(x-1, y+1, dir)
        elif dir == NW:
            return Pos(x-1, y-1, dir)
        elif dir is None:
            return Pos(x, y, dir)

class Game(Board):
    def solve(self, start, end, path=None):
        #print(path)
        if path is None:
            path = [] #frozenset()
        if start[:2] == end[:2]:
            yield path + [start]
            return
        if start in path:
            return
        if self[start] == '.':
            return
        if self[start] in 'AEIOUY':
            rot = 1
        else:
            rot = -1
        mild = self.neighbor(start, start.dir.rotate(rot))
        yield from self.solve(mild, end, path + [start])
        sharp = self.neighbor(start, start.dir.rotate(2*rot))
        yield from self.solve(sharp, end, path + [start])

game = Game()
start = Pos(1, len(MAZE)-4, SE)
assert game[start] == 'D'
end = Pos(1, 2, None)
assert game[end] == '@'
for path in game.solve(start, end):
    s = '\n'.join(f'{game[pos]} ({pos.x}, {pos.y}) {pos.dir}' for pos in path)
    s = ' '.join(pos.dir.name for pos in path)
    print(s)
    print(f'-- {len(path)} moves --')
    print()

print()
print('--------')
print()

m = Pos(2, 9, None)
assert game[m] == 'M'
for path in game.solve(start, m):
    s = '\n'.join(f'{game[pos]} ({pos.x}, {pos.y}) {pos.dir}' for pos in path)
    s = ' '.join(pos.dir.name for pos in path)
    print(s)
    print(f'-- {len(path)} moves --')
    print()

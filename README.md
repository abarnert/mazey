# mazey
Solve the maze at https://fivethirtyeight.com/features/can-you-escape-this-enchanted-maze/

# Representing the problem

This looks like a simple graph of hexes, but it's actually a graph of hex-and-direction nodes. Visiting the same hex again isn't a cycle unless you're visiting it in the same direction.

But there's no need for an explicit graph. I just stored the hexes in a 2D array (or list of lists; it didn't seem worth pulling in numpy), used (x, y, direction) tuples as nodes, and left the edges implicit in the algorithm.

Figuring out how to render that array in text in a readable-enough format to check for typos was a bit annoying.

# Solving the problem

Ignoring the M rule, it's just a trivial brute-force recursive graph search. At each point, there are four possibilities:

 * Win!: the current path is a solution
 * Off the edge/grey: no solutions from here
 * Already-visited hex+direction: no solutions from here (except ones we'll already see elsehwere)
 * Anything else: all solutions at the mild turn, and all solutions at the sharp turn

The M rule at first seems like it means you need to filter the paths. But, because falling off the edge means you start over, rather than losing, any path from start to M to an edge plus any path from start to win works. (There's no other benefit of falling off the edge, because there's no other hex we have to go through.) The problem deosn't even ask for the shortest path.

But getting the shortest path is pretty simple. It's the shortest start-to-win-through-M path, or the shortest start-to-win plus the shortest start-to-m-to-edge, whichever is shorter. I didn't even bother writing code for that, because there are few enough paths that you can inspect manually.

There are 3 start-to-win paths, the shortest being length 25. None pass through M. There are actually a ton of start-to-M paths, but you can tell by immediate inspection that a 4-move path is going to work, and can't be beaten. 

So, first hit the M. Including the initial SE move from "Start u r here" to D, the directions are:

    SE N NE N
    
And the letters are:
    
    D A M off-the-edge

Then take the 25-move path from "Start u r here" to Win!

    SE N SE SW SE N NE N SE NE SE N NW N NW NE S SE SW NW SW N NW SW N

Where the letters are:

    D A A D Q A N Y C E N S E K U E K E E S A L F I Win!

(Notice that we do need to cycle through the same hex at a different facing a few times.)

# Improvements?

If this weren't something I slapped together in under and hour and was never going to run again because there are no other mazes to solve:

 * Implement the M-checking, and start-to-M-to-restart-to-win, in code.
 * The code is a bit of a miss.
 * Store the letters in the Pos objects so they can be printed usefully without needing the board object.
 * Come up with a less ugly and more compact way to display the paths.
 * Maybe actually display things ASCII-graphically.
 * Double-check for typos in the input.
 * Implement a second algorithm to verify that this one did the right thing.

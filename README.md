# Wave Function Collapse Experimentation

## A Sudoku Solver using WFC

Currently it's slightly modified since potential values aren't stored and removed from, but rather requested on each iteration.
But, I think it fits with WFC as I undestand it.
It currently solves "Easy" problems I copied from [sudoku.com](sudoku.com).
I haven't tried on anything more difficult.
Efficiency probably could be improved.
At present the `sudoku` value in the tests is solved in 42 iterations and the entire test suite runs in 0.06s on my machine.
(Though in the event a guess is made where the answer isn't known there is some randomness.)

The current implementation has been slightly modified as it doesn't store and remove potential values, but rather requests them on each iteration. 
However, I believe it aligns well with my understanding of WFC. 
It can currently solve "Easy" problems taken from [sudoku.com](sudoku.com).
I have yet to test it on anything more challenging. 
There is room for improvement in terms of efficiency. 
As of now, the `sudoku` value in the tests is solved in 42 iterations and the entire test suite runs in 0.06 seconds on my machine. 
Note that there is some randomness involved in the event of a guess being made where the answer is unknown.

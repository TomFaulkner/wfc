# Wave Function Collapse Experimentation

## A Sudoku Solver using WFC

The current implementation has been slightly modified as it doesn't store and remove potential values, but rather requests them on each iteration. 
However, I believe it aligns well with my understanding of WFC. 
It can currently solve "Easy" problems taken from [sudoku.com](sudoku.com).
I have yet to test it on anything more challenging. 
There is room for improvement in terms of efficiency. 
As of now, the `sudoku` value in the tests is solved in 42 iterations and the entire test suite runs in 0.06 seconds on my machine. 
Note that there is some randomness involved in the event of a guess being made where the answer is unknown.

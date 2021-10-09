<hr>

# Search Problems

## 1. Missionaries and Cannibals
- DFS
- BFS
- Iterative Deepening Search

<img src='./Search Problems/m&c.PNG'>

<hr>

## 2. Eight Puzzle

- Uninformed Searches <br> **VS**
- Greedy Search : Heuristic methods - DFS
- A* Search Algorithm

<img src='./Search Problems/8-puzzle.PNG'>

<br>
<br>

<hr>

# Game Problems

## 1. Four in a Row

- Min-max with Alpha-Beta Pruning
- Monte-Carlo Tree Search   
- Time based/Depth Limit Game 

#### Run/Change Algorithms in
-  Game_CSP Problems/Four in a row/run_assignment2.py 

<img src='./Game_CSP Problems/Four in a row/connect-four.PNG'>

<hr>

## 2. CSP : 

- Game_CSP Problems/zebra_puzzle.pl
- Prolog Scistus Implementation of who is living where, what they
smoke, drink and their pets etc

#### Example
- The man who smokes Blend lives in the house next to the house with cats.
```
- Blend #= Cats +1 #\/ Blend #= Cats - 1,  %Can be either side so OR \/
```
- Output after different constrains
```
| ?- zebra.
house 1        house 2        house 3        house 4        house 5
1-yellow       2-blue         3-red          4-green        5-white
1-norwegian    2-dane         3-english      4-german       5-swede
1-dunhill      2-blend        3-pall_mall    4-prince       5-blue_master
1-water        2-tea          3-milk         4-coffee       5-beer
1-cats         2-horse        3-birds        4-zebra        5-dog
yes
```

<hr>

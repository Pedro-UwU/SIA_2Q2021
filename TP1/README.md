# IA Search Algorithms
This is an Artificial Intelligence Systems' project for the Buenos Aires Institute of Technology (ITBA)

###Objectives
Utilize different search algorithms to solve different Sokoban games.
Sokoban is a puzzle video game genre in which the player pushes crates or boxes around in a warehouse, trying to get them to storage locations. [Wiki](https://en.wikipedia.org/wiki/Sokoban)

###How to run the project
To be able to run the code you will need to have Python 3.6 or later versions installed. Once you have it, all you need to do is go to the working directory (where the main.py is located) and run the following command in the terminal
```
> python3 ./main.py
```

###Config file
The file 'config.conf' can be used to tweak and modify different parameters.
These are:
- **BOARD_FILE_PATH**: Path to the file whit the Sokoban's board to solve
- **SEARCH_FUNCTION**: The search function that will be used (listed in the next section)
- **CHECK_DEADLOCKS_WITH_UNINFORMED**: Flag to check deadlock states while using uninformed search functions
- **OUTPUT_FILE_NAME**: Name of the output file (must contain file type)
- **PRINT_ON_TERMINAL**: Flag to indicate if the solution should be printed on terminal or not
- **PRINT_WITH_COLORS**: Flag to indicate if the printed solution should contain colors or not (may not work in some Operative Systems)
- **HEURISTIC**: Name of the heuristic function that will be used with the informed search algorithms (listed in their section)

The name of the search function and heuristic functions must be spelled **exactly** as to how they are listed below

###Search Functions:
This is the list of the available search functions:
- **Uninformed Search**
    - **BFS**: Breadth first search
    - **DFS**: Deep first search
    - **IDDFS**: Iterative deepening depth-first search
- **Informed Search**:
    - **Greedy**: Local greedy search using heuristics
    - **A Star**: A\* algorithm
    - **IDA Star**: Iterative  deepening A\* algorithm
    
###Heuristics
This is the list of the heuristic functions:
- **Distance**: Sum of the Manhattan distance of each box with its closest goal
- **Steps**: Sum of the necessary steps of each box with its closest goal
- **Minmatching**: Minimal bipartitioning match between all boxes and goals. [Source](https://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=8BA204ED92639C0447CE1A5DE3D62E59?doi=10.1.1.46.947&rep=rep1&type=pdf) (Section 4.3: "Lower Bound Heuristic") Author: Andreas Junghanns 

###What we learned?
This project made us be informed and implement different search algorithms and techniques to solve this kind of problems.
It represents a very useful tool to have in the future of our careers, and it showed us that search algorithms can be complex but with enough work, you can design an elegant and useful solution
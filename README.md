﻿# <center> **Artificial Intelligence** <center/>
## **Project 1: Search**
<br>

![search](https://user-images.githubusercontent.com/79363930/159104681-af1dc271-e65b-4ae2-837e-3a30c53c5fe6.png)

<br>

*Subject: Fundamentals of Artificial Intelligence*
<br>
*Lecture: Bui Tien Len*
<br>
*TA: Nguyen Thai Vu*
<br>
*Student: Dang Ngoc Tien - 20127641*

<br>

**1. Introduction**
<br>
In this project, students research and implement the searching algorithm. In addition, students have to visualize the result of the searching algorithm.
<br>
<br>

**2. Requirements**
<br>
- Individual project.
- Programming language: Python (for visualization, we recommend students
use turtle library of Python)
- Timeline: 2 weeks.
  -  Code folder: include every coding files.
  -  Report folder: include file report.pdf:
     -  Student’s information
     -  Each algorithm, student report:
        -  The idea of the algorithm.
        -  Example (reference section input/output)
        -  Conclusion, pros and cons.
-  Evaluation:
   -  Implement 5 searching algorithm: 70%.
   -  Report: 30%
-  Every cheat/copy/lie will be punished with a course score of 0.
<br>

**3. Problem**
<br>

a. Problem description
-  The robot has been sent to a maze of size M x N, and the robot has to find the path from the Source (starting position) to the Goal (ending position). The robot allows to move in 4 directions: up, down, left, right. In the maze, there are some obstacles.
-  The student as asked to implement 5 search algorithms:
   -  Breadth-first search
   -  Uniform-cost search
   -  Iterative deepening search that uses depth-first tree search as core
component and avoids loops by checking a new node against the
current path.
   -  Greedy-best first search using the Manhattan distance as heuristic.
   -  Graph-search A* using the Manhattan distance as heuristic.
<br>

b. Input/output format
-  The format of the input file:
   -  First line: the size of the maze width, height.
   - Second line: the position of the Source and Goal. For example: 2 2 19 16 meaning source point is (2, 2) and goal point is (19, 16).
  - Third line: the number of the obstacles in the maze.
  - The next following line, defining the obstacle by the rule:
    - The obstacle is a Convex polygon.
    - A polygon is a set of points that are next to each other clockwise. The last point will be implicitly concatenated to the first point to form a valid convex polygon.
-  The output:
   - Graphical representation of polygons and path.
   - Cost.
- The example of input.txt
  
    *(Everything is relative, depend on your implementation)*
    
    22 18 <br>
    2 2 19 16 <br>
    3 <br>
    4 4 5 9 8 10 9 5 <br>
    8 12 8 17 13 12 <br>
    11 1 11 6 14 6 14 1 <br>

    ![search](https://user-images.githubusercontent.com/79363930/191313177-064be147-6423-4dab-8e83-3fc933c45bfa.png)


**4. References**

The document in the Computer Science Department at the University of
Science, Vietnam National University, Ho Chi Minh City.

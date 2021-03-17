# KX_Assignment
The python file "algorithm_assigment.py" is where you can find the Algorithmic Task

## Task Description
You can find the description of the task in [this pdf](task_description/KX_Assignment.pdf)

## Solution
To solve the problem, the program propagates the information of the colors of the graph, in such a way that each link knows if in one direction it can find blue or red edges. In the image below the arrows represents the direction in which the links can find both a blue and a red color.
With these arrows you can find most of the paths but not all of them. To find them all, it is necessary to cut the graph and perform more iterations until no more paths are found, as shown in the image.

## Comand:
    python3 algorithm_assigment.py ./relative_path_to_in_file
for example: python3 algorithm_assigment.py ./data_cases/case_05.in



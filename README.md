![TITLE_pic](https://github.com/AgentDS/AIMA-CSCI-561-18fall/raw/master/TITLE_pic.png)
# Artificial Intelligence: A Modern Approach -- CSCI 561 2018fall

by Prof. Sheila Tejada

[![Build Status](https://travis-ci.com/AgentDS/AIMA-CSCI-561-18fall.svg?token=Zdxzuh6yQ7NxpAUZUUKb&branch=master)](https://travis-ci.com/AgentDS/AIMA-CSCI-561-18fall)

[Travis CI Link](https://travis-ci.com/AgentDS/AIMA-CSCI-561-18fall)

Python implementation for CSCI 561 Foundations of Artificial Intelligence 2018fall assignments.

### Finished Currently

- [HW1a](./HW1a): Simple Reflex Agent ([description](./HW1a/HW1a.pdf)) 

- [HW1b](./HW1b): Pilot Scooter Program ([description](./HW1b/HW1b.pdf)) 

  =>  _stupid permutation_ edition finished

  =>  _smart recursive_ edition finished, not fast enough

- [HW2](./HW2): SPLA & LAHSA ([description](./HW2/F18HW2_V2.pdf))

  => Without any pruning

- [HW3](./HW3): MDP problem in SpeedRacer ([description](./HW3/F18HW3 UPDATED.pdf))

  => Be able to run the largest test case [input11.txt](./HW3/HW3_Test_Cases/input11.txt) (100x100 grids, 8 cars) in 1min on Vocareum platform by updating all utility value at once for each iteration using 4D numpy array of shape $s \times s \times 4 \times 4$, where $s$ is the row/column size of the grid. (Without this method, it might take more than 11min for input11.txt)


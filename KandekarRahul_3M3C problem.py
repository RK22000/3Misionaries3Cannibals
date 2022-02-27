# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 19:16:07 2022

@author: rahul
"""

def bfs(root, targetState, stateFunc=lambda z:z.state, nodelimit=100, verbose=False):
    """Function to perform bfs on a node.
    :param Node root: root Node with properties: state and getNeighbours()
    :param targetState: the state of the solution node
    :param stateFunc: function that maps a Node to its state
    :param nodelimit: limit on the total number of Nodes allowed to be generated
    :param verbose: True if every visited node should be printed
    :returns: the target node or None, list of all the visited nodes in order of visit, maximum number of nodes stored at once, number of nodes generated"""
    queue = [root]
    seen = set()
    visited = []
    generated = 0
    maxStored = 0
    while len(queue) > 0:
        maxStored = max(maxStored, len(queue))

        # Pop the queue and check if it is the correct node
        node = queue.pop(0)
        if stateFunc(node) == targetState:
            return node, visited, maxStored, generated

        # If not the correct node then add its children to the queue
        for neighbour in node.getNeighbours():
            generated += 1
            if not neighbour.state in seen:
                queue += [neighbour]
                seen.add(neighbour.state)
        
        if(verbose): print(str(node))
        visited += [node]
        nodelimit-=1
        if nodelimit==0: break
    return None, visited, maxStored, generated

def dfs(root, targetState, stateFunc=lambda z:z.state, nodelimit=100, depthlimit=100, verbose=False):
    """Function to perform dfs on a node.
    :param Node root: root Node with properties: state and getNeighbours()
    :param targetState: the state of the solution node
    :param stateFunc: function that maps a Node to its state
    :param nodelimit: limit on the total number of Nodes allowed to be generated
    :param depthlimit: max depth the dfs search to descend to
    :param verbose: True if every visited node should be printed
    :returns: the target node or None, list of all the visited nodes in order of visit, maximum number of nodes stored at once, number of nodes generated"""
    stack = [(root, 0)]
    seen = set(root.state)
    visited = []
    generated = 0
    maxStored = 0
    while len(stack) > 0:
        maxStored = max(maxStored, len(stack))
        
        node, depth = stack.pop()
        if stateFunc(node) == targetState:
            return node, visited, maxStored, generated
        if depth==depthlimit: continue
        for neighbour in node.getNeighbours():
            generated += 1
            if not neighbour.state in seen:
                stack += [(neighbour, depth+1)]
                seen.add(neighbour.state)
        
        if(verbose): print((str(node), depth))
        visited += [node]
        nodelimit-=1
        if nodelimit==0: break
    return None, visited

M,C=0,1
class RiverNode:
    """Class to represent each situation of the river problem as a Node"""
    def __init__(self, state, parent=None, action="[Start]"):
        """
        :param state: Initial state of the RiverNode
        :param parent: The Node parent to this node
        :param action: The action that leads from parent node to this node
        """
        self.state = state # (((missionaries on left bank, cannibals on left bank) , (missionaries on right bank, cannibals on right bank)), boat position) 0=left, 1=right
        self.parent = parent
        self.action = action
        self.neighbours = None
        
    def getNeighbours(self):
        if self.neighbours == None:
            self.findNeighbours()
        return self.neighbours
    
    def findNeighbours(self):
        self.neighbours=[]
        boatpos = self.state[1]
        people = self.state[0][boatpos]
        direction = ("go right by boat", "go left by boat")
        for m in range(min(3, people[M]+1)): # m will be the number of missionaries leaving on the boat
            for c in range(min(3-m, people[C]+1)): # c will be the number of cannibals leaving on the boat
                if m+c==0: continue
                action = f"[{m} M, {c} C {direction[boatpos]}]"         # [1 M, 1 C go right by boat]
                boatside = (people[M]-m, people[C]-c) # People remaining on boatside
                otherside=((3-boatside[M]), (3-boatside[C])) # People now on the other side
                if(boatpos==0):
                    banks = (boatside, otherside)
                else: banks = (otherside, boatside)
                state = (banks, 1-boatpos)
                neighbour = RiverNode(state=state, parent=self, action=action)
                if(neighbour.safeState()):
                    self.neighbours += [neighbour]
    
    def safeState(self):
        lside, rside = self.state[0]
        return ( lside[M]>=lside[C] or lside[M]==0 ) and ( rside[M]>=rside[C] or rside[M]==0 )
    
    def __str__(self):   # [1 M, 1 C go right by boat] => [2 M, 2 C - 1 M, 1 C]
        l, r = self.state[0][0], self.state[0][1]
        return f"{self.action} => [{l[M]} M, {l[C]} C - {r[M]} M, {r[C]} C]"
    
    def getPathFromRoot(self):
        if self.parent == None:
            return [self]
        return self.parent.getPathFromRoot() + [self]

def main():
    algorithm = input("Select a search algorithm (bfs/dfs): ")
    search, txt = (bfs, "bfs") if algorithm == "bfs" else (dfs, "dfs")
    root = RiverNode(state=(((3,3), (0,0)), 0))
    target, visited, maxStored, generated = search(root=root, targetState=((0,0),(3,3)), stateFunc=lambda z:z.state[0])
    solution = "\n".join( [ str(i+1) + ". " + str(x) for i, x in enumerate(target.getPathFromRoot()) ] )

    print(f"\n{txt} Solution:\n{solution}\n")
    print(f"{generated} nodes were generated and the maximum number of nodes stored were {maxStored}")
    input("Hit Enter to exit")

if __name__ == '__main__':
    main()
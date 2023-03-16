
# from __future__ import print_function
from ortools.sat.python import cp_model as cp
import math, sys
from cp_sat_utils import scalar_product
from scipy import sparse
import numpy as np

def main():

  model = cp.CpModel()
  #
  # data
  #
  
  n_subset = 4  # number of subsets
  n_nid = 6  # number of dst nodes

  Adj = [[2,3],[2],[0,1,4],[0,2,5]]   # subset row, nid col
  mtx = sparse.lil_matrix((n_subset, n_nid)) # matrix : 4*6
  for i in range (len(Adj)):
    mtx[i,Adj[i]] = np.ones(len(Adj[i]))
  
  T_mtx= mtx.transpose()
  # print(T_mtx.todense()) 
  # print(T_mtx.rows)
  transposeAdj = T_mtx.rows


 
  # transposeAdj = [[2,3],[2],[0,1,3],[0],[2],[3]] # nid: row, subsets: col
  
  # Cost = [1, 1, 1, 1] # each subsets' weight
  
 
  # n_subset = 6
  # n_nid = 7
  Cost = np.ones(n_subset)
  # transposeAdj = [[2, 3], [2], [0, 1, 3], [0], [2], [3]]
  transposeAdj = [list([1]) list([0, 2, 5]) list([1, 3]) list([1, 2, 4]) list([1, 2, 3]) list([1]) list([3])]
  SUBSET_ID = list(range(n_subset))
  NID = list(range(n_nid))

  print('transposeAdj ', transposeAdj)
  #
  # variables
  #
  Use_subset = [model.NewBoolVar("Use_subset[%i]" % w) for w in SUBSET_ID]
  total_cost = model.NewIntVar(0, n_subset * sum(Cost), "total_cost")

  #
  # constraints
  #
  scalar_product(model, Use_subset, Cost, total_cost)

  for j in NID: # NID : dst nodes
    # Sum the cost for use the subsets 

    # print('j',j)
    tmp = [Use_subset[c] for c in transposeAdj[j]]
    # print(tmp)
    print()
    print("row "+str(j)+ ' -----'+ str(sum(tmp)))

    model.Add(sum([Use_subset[c ] for c in transposeAdj[j]]) >= 1)

  # objective: Minimize total cost
  model.Minimize(total_cost)

  #
  # search and result
  #
  solver = cp.CpSolver()
  status = solver.Solve(model)
  
  if status == cp.OPTIMAL:
    print("Total cost", solver.Value(total_cost))
    print("We should use these subsets: ", end=" ")
    for w in SUBSET_ID:
      if solver.Value(Use_subset[w]) == 1:
        print(w, end=" ")
    print()

  print()
  print("NumConflicts:", solver.NumConflicts())
  print("NumBranches:", solver.NumBranches())
  print("WallTime:", solver.WallTime())


if __name__ == "__main__":
  main()


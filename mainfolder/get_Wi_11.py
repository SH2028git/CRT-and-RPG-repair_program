def get_Wi(G,A):
    n = int((G.number_of_nodes()-2)/2)
    #print(A)
    #print(n)
    Repair_Wi = sum(2**(2*n - x) for x in A if x!=2*n+1)
    #print(Repair_Wi)
    return Repair_Wi
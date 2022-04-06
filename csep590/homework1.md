Suggestions
    What are the shortcomings of previous approaches that this paper addresses?
    What are assumptions made by their new algorithm??
    A subtle bug was reported in algorithm EnumerateCmp. What is that bug?


About Results
    If we had to chose one algorithm to implement then DPccp is a good choice for chain, cycle, clique and star queries. However, DPccp is mainly performant for star queries, while DPsize is performant for chain and cycle and DPsub is performant for clique queries.

About the bug
    Referring to errata we see that the EnumerateCmp algorithm excludes enumerating complements for a given connected subgraph S. It is interesting that the errata identifying the bug was published about 12 years after the original paper.

Summary of the paper
    The paper presents 3 algorithms - DPsize, DPsub and DPccp.

    Is DPccp implemented by commericial DBMS?
    

    It is interesting to see that the EnumerateCsg and EnumerateCmp algorithms can be applied to any undirected graph thus implying its application beyond query optimizers.
import numpy as np
import networkx as nx


def trace_lcs(xs, ys):
    # initialize
    xs_ = "-" + xs
    ys_ = "-" + ys
    n = len(xs_)
    m = len(ys_)

    print("x: " + str(xs))
    print("y: " + str(ys))

    lcs_num = np.zeros((n, m), dtype=int)
    lcs_trace = nx.DiGraph()
    initial_edges_low = [((k, 0), (k-1, 0)) for k in range(1, n)] + [((k, 1), (k-1, 1)) for k in range(1, n)]
    initial_edges_line = [((0, l), (0, l-1)) for l in range(1, m)] + [((1, l), (1, l-1)) for l in range(1, m)]
    lcs_trace.add_edges_from(initial_edges_low + initial_edges_line)

    # (k,1)/(1,k)成分 k=0,...,n-1
    if xs_[1] == ys_[1]:
        for i in range(0, n):
            lcs_num[i][1] = 1
            lcs_num[1][i] = 1

    # (i,j)成分 i=2,...,n-2 j=2,...,n-2
    for i in range(2, n-1):
        for j in range(2, m-1):
            delta = 1 if xs_[i] == ys_[j] else 0
            topleft = lcs_num[i-2][j-2] + delta
            left = lcs_num[i][j-1]
            top = lcs_num[i-1][j]
            if delta == 1:
                lcs_num[i][j] = topleft
                lcs_trace.add_edge((i, j), (i-2, j-2))
            if left >= topleft and left >= top:
                lcs_num[i][j] = left
                lcs_trace.add_edge((i, j), (i, j-1))
            if top >= left and top >= topleft:
                lcs_num[i][j] = top
                lcs_trace.add_edge((i, j), (i-1, j))

    # (i,m)成分 i=2,...,n-2
        j = m-1
        lcs_num[i][j] = lcs_num[i][j-1]
        lcs_trace.add_edge((i, j), (i, j-1))

    # (n,j)成分 j=2,...,m-2
    i = n-1
    for j in range(2, m-1):
        lcs_num[i][j] = lcs_num[i-1][j]
        lcs_trace.add_edge((i, j), (i-1, j))
    # (n,m)成分
    j = m-1
    if xs_[i] == ys_[j]:
        lcs_num[i][j] = lcs_num[i-2][j-2] + 1
        lcs_trace.add_edge((i, j), (i-2, j-2))
    else:
        lcs_num[i][j] = lcs_num[i-1][j-1]
        lcs_trace.add_edge((i, j), (i-1, j-1))

    print("結果:")
    print(lcs_num)
    # print("all paths:")
    # for path in nx.all_simple_paths(lcs_trace, source=(n-1, m-1), target=(0, 0)):
    #    print(path)
    print("lcsの長さ: " + str(lcs_num[-1][-1]))

    def show_generalized_sequence(trace):  # (n,m)から(0,0)へのパス(リスト)のリスト
        def extract_tuple(path):  # list -> tuple
            def addt(t1: tuple, t2: tuple):
                return t1[0] + t2[0], t1[1] + t2[1]

            def iter_(li: list):
                if len(li) == 1:
                    return ()
                last = li[-1]
                remain = li[0:-1]
                sndlast = remain[-1]
                if addt(last, (2, 2)) == sndlast:
                    return (sndlast,) + iter_(remain)
                else:
                    return iter_(remain)
            return iter_(path)

        allpath = set(map(extract_tuple, trace))

        print('共通文字列')
        paths = set()
        for path in allpath:
            com_seq = '-'
            for node in path:
                if node == (2, 2):
                    com_seq = xs_[node[0]]
                elif node == (n-1, m-1):
                    com_seq += xs_[node[0]]
                else:
                    com_seq += xs_[node[0]] + '-'
            paths.add(com_seq)

        for path in paths:
            print(path)

    show_generalized_sequence(nx.all_simple_paths(lcs_trace, source=(n-1, m-1), target=(0, 0)))


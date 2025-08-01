import pydot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tempfile
import os

def hasse(imp, n_items, dir_path = 'plots/', labels = None):
    """
    Hasse diagram of Surmise Relation
    Plots the Hasse diagram of surmise relation.

    :param imp: list of implications
    :param n_items: number of items of the domain
    :param dir_path: path to the png directory
    :param labels: string labels for items
    :return: produces a plot and returns a list of the equally informative items
    """

    parallel_items = {}
    implications = list(imp)

    # generate partially ordered set
    for i in implications:
        if (i[1], i[0]) in implications:
            if i[0] in parallel_items:
                parallel_items[i[0]].append(i[1])
            else:
                parallel_items[i[0]] = [i[0], i[1]]
            implications.remove(i)
            implications.remove((i[1], i[0]))
            for j in range(len(implications)):
                if i[1] == implications[j][0]:
                    implications[j] = (i[0], implications[j][1])
                elif i[1] == implications[j][1]:
                    implications[j] = (implications[j][0], i[0])

    implications = list(set(implications))
    # remove reflexive properties
    for i in list(implications):
        if i[0] == i[1]:
            implications.remove(i)

    #   i    j     k
    # (0,1)(1,2),(0,2)
    # remove transitive properites
    for i in list(implications):
        for j in list(implications):
            for k in list(implications):
                if i[1]==j[0] and j[1]==k[1] and i[0]==k[0]:
                    implications.remove(k)

    for i in list(implications):
        for j in range(n_items):
            if (i[0] != j) and (i[1] != j) and ((i[0], j) in implications) and ((i[1], j) in implications):
                implications.remove((i[0], j))

    # bottom-up approach
    for i in range(len(implications)):
        implications[i] = (implications[i][1], implications[i][0])
    print(implications)
    
    #graph = pydot.Dot(graph_type='graph')
    graph = pydot.Dot(graph_type='digraph', rankdir='BT')  # Makes diagram grow upward
    if labels:
        for i in implications:
            graph.add_edge(pydot.Edge(str(labels[int(i[0])]), str(labels[int(i[1])]), arrowhead='normal'))
    else:
        for i in implications:
            graph.add_edge(pydot.Edge(i[0], i[1], arrowhead='normal'))

    # standalone nodes (with label support)
    for i in range(n_items):
        found = any(i in implication for implication in implications)
        if not found:
            parallel = any(i in value for value in parallel_items.values())
            if not parallel:
                label = str(labels[i]) if labels else str(i)
                graph.add_node(pydot.Node(label))


    fout = tempfile.NamedTemporaryFile(mode = 'w+t', dir = dir_path, suffix=".png", delete = False)
    graph.write(fout.name, format="png")
    img = mpimg.imread(fout.name)
    plt.axis('off')
    plt.imshow(img)
    plt.show()
    #os.remove(fout.name)

    return [list(set(value)) for key, value in parallel_items.items()]

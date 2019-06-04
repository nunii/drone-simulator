import networkx as nx
from matplotlib import pyplot as plt


class SLAMGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_point(self, name,  data):
        """add a new point of interest.

        :return: a class object, self.
        :rtype: SLAMGraph
        """
        self.graph.add_node(name, data=data)
        return self

    def add_edge(self, from_node,  to_node, distance: float):
        """add a new edge between two nodes with weights.

        :param from_node: a source node name.
        :param to_node: a destination node name.
        :param distance: a distance between two nodes.
        :return: a class object, self.
        :rtype: SLAMGraph
        """
        self.graph.add_edge(from_node, to_node)
        self.graph[from_node][to_node]['weight'] = distance
        return self

    def get_neighbors(self, node_name):
        """get a neighbors of a required node.

        :param node_name: a name of a node.
        :return: a neighbors names.
        :rtype: list
        """
        return list(self.graph.neighbors(node_name))

    def get_data(self, node_name):
        """get a data stored in a node.

        :param node_name: a required node name.
        :return: a data.
        :rtype: dict
        """
        return self.graph.nodes[node_name]['data']

    def shortest_path(self, source, target):
        """get the shortest path between two node, using 'dijkstra'.

        :param source: a name of source node.
        :param target: a name of target node.
        :return: a shortest list from source node to target.
        :rtype: list.
        """
        return nx.shortest_path(self.graph, source=source, target=target)

    def show(self):
        """show graph."""
        nx.draw(self.graph)
        plt.show()

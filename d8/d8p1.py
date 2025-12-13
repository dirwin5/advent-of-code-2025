"""
https://adventofcode.com/2025/day/8
"""
import pathlib
from time import time
import math


class Node:
    def __init__(self,
                 node_id: str):
        self.node_id = node_id
        self.connected_links = []

    def add_link(self,
                 link: 'Link'):
        self.connected_links.append(link)


class Link:
    def __init__(self,
                 link_id: int,
                 node1: Node,
                 node2: Node):
        self.link_id = link_id
        self.node1 = node1
        self.node2 = node2

    def get_connected_nodes(self):
        return [self.node1, self.node2]

    def print_connected_nodes(self):
        print(self.node1.node_id)
        print(self.node2.node_id)


class Circuit:
    def __init__(self):
        self.links = []
        self.nodes = []

    def build_circuit(self,
                      starting_link: Link):
        # recursively find all links connected to current circuit
        self.links.append(starting_link)
        nodes_to_check = []
        nodes_to_check.extend(starting_link.get_connected_nodes())
        while len(nodes_to_check) > 0:
            current_node = nodes_to_check.pop()
            connected_links = current_node.connected_links
            for link in connected_links:
                if link not in self.links:
                    self.links.append(link)
                    nodes_to_check.extend(link.get_connected_nodes())
        # build node list
        self._build_nodes_list()

    def _build_nodes_list(self):
        for link in self.links:
            self.nodes.extend(link.get_connected_nodes())
        self.nodes = list(set(self.nodes))

    def get_circuit_length(self) -> int:
        return len(self.links)


def strip_lines(lines_list: list[str]) -> list[str]:
    stripped_lines_list = []
    for item in lines_list:
        stripped_lines_list.append(item.strip())
    return stripped_lines_list


def calculate_distance(node1: str, node2: str) -> float:
    x1, y1, z1 = node1.split(',')
    x2, y2, z2 = node2.split(',')
    x_delta = abs(int(x1) - int(x2))
    y_delta = abs(int(y1) - int(y2))
    z_delta = abs(int(z1) - int(z2))
    distance = x_delta ** 2 + y_delta ** 2 + z_delta ** 2
    return math.sqrt(distance)


def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')
    # input_file = input_dir.joinpath('sample_input.txt')

    # read input file
    with open(input_file, 'r') as f:
        node_list = f.readlines()

    # strip leading and trailing whitespace
    node_list = strip_lines(node_list)

    # iterate over every combination of nodes and create list
    distances = []
    link_id = 0
    while True:
        current_node = node_list.pop()
        for node in node_list:
            distance = calculate_distance(current_node, node)
            distances.append((distance, current_node, node, link_id))
            link_id += 1
        if len(node_list) == 0:
            break

    # sort distances by first item in each tuple
    sorted_distances = sorted(distances, key=lambda n: n[0])

    # only keep shortest 1000 (10 for sample)
    shortest_distances = sorted_distances[:1000]

    # build nodes and links dicts
    link_dict = {}
    node_dict = {}
    for link_tuple in shortest_distances:
        node1_id = link_tuple[1]
        node2_id = link_tuple[2]
        link_id = link_tuple[3]

        # check if node object exists yet, and create if not
        if node1_id not in node_dict:
            node1 = Node(node1_id)
            node_dict[node1_id] = node1
        else:
            node1 = node_dict[node1_id]
        if node2_id not in node_dict:
            node2 = Node(node2_id)
            node_dict[node2_id] = node2
        else:
            node2 = node_dict[node2_id]

        # create link object and add to link_dict
        link = Link(link_id = link_id, node1=node1, node2=node2)
        link_dict[link_id] = link

        # add connected link to nodes
        node1.add_link(link)
        node2.add_link(link)

    # build circuits for each link
    circuits_list = []
    circuits_node_counts = []
    seen_links = []

    for link in link_dict.values():
        if link in seen_links:
            continue
        # create new circuit
        current_circuit = Circuit()
        current_circuit.build_circuit(link)
        circuits_list.append(current_circuit)
        # count how many nodes are in this circuit
        node_count = len(current_circuit.nodes)
        circuits_node_counts.append(node_count)
        seen_links.extend(current_circuit.links)

    circuits_node_counts = sorted(circuits_node_counts)

    largest_circuits = circuits_node_counts[-3:]
    total = math.prod(largest_circuits)

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Largest circuits: {largest_circuits}')
    print(f'Total: {total}')


if __name__ == "__main__":
    main()
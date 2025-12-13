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
                 node2: Node,
                 length: float):
        self.link_id = link_id
        self.node1 = node1
        self.node2 = node2
        self.length = length

    def get_connected_nodes(self):
        return [self.node1, self.node2]

    def print_connected_nodes(self):
        print(f'{self.node1.node_id} and {self.node2.node_id}: {self.length}')


class Circuit:
    def __init__(self, circuit_id):
        self.links = []
        self.nodes = []
        self.circuit_id = circuit_id

    def _add_nodes(self,
                   nodes: list[Node]):
        self.nodes.extend(nodes)
        self.nodes = list(set(self.nodes))

    def add_link(self,
                 link: Link):
        self.links.append(link)
        self._add_nodes(link.get_connected_nodes())

    def build_circuit_in_order(self,
                               sorted_links: list[Link],
                               target_node_count: int):
        for link in sorted_links:
            self.links.append(link)
            self._add_nodes(link.get_connected_nodes())
            if len(self.nodes) >= target_node_count:
                break

    def build_circuit(self,
                      starting_link: Link,
                      target_node_count: None | int = None):
        # recursively find all links connected to current circuit
        self.links.append(starting_link)
        nodes_to_check = []
        nodes_to_check.extend(starting_link.get_connected_nodes())
        self._add_nodes(nodes_to_check)
        while len(nodes_to_check) > 0:
            current_node = nodes_to_check.pop()
            connected_links = current_node.connected_links
            for link in connected_links:
                if link not in self.links:
                    self.links.append(link)
                    link.print_connected_nodes()
                    nodes_to_check.extend(link.get_connected_nodes())
                    self._add_nodes(link.get_connected_nodes())
            if target_node_count:
                if len(self.nodes) >= target_node_count:
                    break

    def _build_nodes_list(self):
        for link in self.links:
            self.nodes.extend(link.get_connected_nodes())
        self.nodes = list(set(self.nodes))

    def get_circuit_length(self) -> int:
        return len(self.links)

    def find_longest_link(self):
        longest_link = self.links[0]
        for link in self.links:
            if link.length > longest_link.length:
                longest_link = link
        return longest_link

    def merge_circuit(self,
                      circuit_to_add: 'Circuit'):
        self.links.extend(circuit_to_add.links)
        self.nodes.extend(circuit_to_add.nodes)
        # remove duplicates
        self.links = list(set(self.links))
        self.nodes = list(set(self.nodes))




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
    number_of_nodes = len(node_list)

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

    # # only keep shortest 1000 (10 for sample)
    # shortest_distances = sorted_distances[:1000]

    # build nodes and links dicts
    link_dict = {}
    node_dict = {}
    sorted_links = []
    for link_tuple in sorted_distances:
        node1_id = link_tuple[1]
        node2_id = link_tuple[2]
        link_id = link_tuple[3]
        link_length = link_tuple[0]

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
        link = Link(link_id = link_id, node1=node1, node2=node2, length=link_length)
        link_dict[link_id] = link
        sorted_links.append(link)

        # add connected link to nodes
        node1.add_link(link)
        node2.add_link(link)

    # add links in order shortest to longest until all nodes are connected
    circuits_dict = {}
    circuit_id = 0
    for i, link in enumerate(sorted_links):
        link.print_connected_nodes()
        circuits_link_is_in = []
        # check if link fits into 1 or more current circuits
        for circuit in circuits_dict.values():
            count = (len(set(link.get_connected_nodes()) & set(circuit.nodes)))
            if count > 0:
                circuits_link_is_in.append(circuit.circuit_id)
        # link not in any existing circuit. Make a new one
        if len(circuits_link_is_in) == 0:
            new_circuit = Circuit(circuit_id)
            new_circuit.add_link(link)
            circuits_dict[circuit_id] = new_circuit
            circuit_id += 1
        # link connected to a single existing circuit without causing multiple circuits to join
        elif len(circuits_link_is_in) == 1:
            circuits_dict[circuits_link_is_in[0]].add_link(link)
        # if link has nodes in 2 circuits, these will merge into one
        elif len(circuits_link_is_in) == 2:
            circuit1 = circuits_dict[circuits_link_is_in[0]]
            circuit2 = circuits_dict[circuits_link_is_in[1]]
            # add link to one circuit first
            circuit1.add_link(link)
            # merge circuits
            circuit1.merge_circuit(circuit2)
            # remove circuit which was merged from dict
            del circuits_dict[circuits_link_is_in[1]]
        else:
            raise RuntimeError("Something went wrong. Unexpected number of matching circuits.")

        # check if we have a single circuit containing all nodes
        if len(circuits_dict.keys()) == 1:
            _, circuit = next(iter(circuits_dict.items()))
            if len(circuit.nodes) == number_of_nodes:
            # if i > 10:
                break

    # find longest link, as this will be added last
    longest_link = circuit.find_longest_link()
    longest_link.print_connected_nodes()

    # multiply x coords
    final_nodes = longest_link.get_connected_nodes()
    x1 = int(final_nodes[0].node_id.split(',')[0])
    x2 = int(final_nodes[1].node_id.split(',')[0])
    total = x1 * x2

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {total}')


if __name__ == "__main__":
    main()

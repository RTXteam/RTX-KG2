"""
    Create a graph from TSV input files (KG2c) and calculate some stats
    for the graph. Write these stats to a JSON report file.

    Usage:
    get_stats_tsv.py <tsv_edge_input_file> <tsv_node_input_file> <output_file_location>
"""


__author__ = 'Timothy Yoon'
__copyright__ = ''
__credits__ = ['Stephen Ramsey', 'Amy Glen', 'Timothy Yoon']
__license__ = ''
__version__ = ''
__maintainer__ = ''
__email__ = ''
__status__ = ''


import argparse
import datetime
import igraph
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os.path
import random


# Dictionary for saving results
# Will be used to create the report file
results = {}


def build_output_file_path(output_file_location):
    """
    :param output_file_location: A string indicating the directory in which
    the output report file should be generated
    :return output_file_path: A string path to the output report file, which
    will later be opened and written to
    """
    file_name = "stats_report_tsv.json"
    output_file_path = ""
    output_file_path += output_file_location

    # If the output_file_location string has a '/' as its final character,
    # append only the file name to create the path
    if output_file_location[len(output_file_location) - 1] == '/':
        output_file_path += file_name

    # Otherwise append a '/' followed by the file name to create the path
    else:
        output_file_path += '/'
        output_file_path += file_name
    
    return output_file_path


def initialize_results_dict(input_file_paths, datetime_str):
    """
    Initialize the global 'results' dictionary.

    :param input_file_paths: A list of the paths to the input files. The first
                             item in the list is the TSV edge input file,
                             followed by the TSV node input file
    :param datetime_str: A string for the current local date and time
    """
    global results

    # Populate the dictionary
    results["_report_datetime"] = datetime_str
    results["script"] = os.path.basename(__file__)  # Current script name
    results["input_files"] = {}
    results["input_files"]["paths"] = input_file_paths
    results["created_graph"] = {}
    results["runtimes"] = {}


def get_tsv_edge_count(input_file_path):
    """
    :param input_file_path: The string path to the TSV edge input file
    :return tsv_edge_count: The number of edges specified in the input file
    """
    tsv_edge_count = 0
    
    with open(input_file_path) as file:
        for line in file:
            tsv_edge_count += 1
    return tsv_edge_count


def get_tsv_node_count(input_file_path):
    """
    :param input_file_path: The string path to the TSV node input file
    :return tsv_node_count: The number of nodes specified in the input file
    """
    tsv_node_count = 0
    
    with open(input_file_path) as file:
        for line in file:
            tsv_node_count += 1
    return tsv_node_count


def build_graph(edge_input_file_path):
    """
    :param edge_input_file_path: The string path to the TSV edge input file
    :return graph: A graph built using the edges specified in the input file
    """
    # If current directory already has a pickled graph, read and return it
    if os.path.isfile("kg2c.pickle"):
        graph = igraph.Graph.Read_Pickle(fname="kg2c.pickle")
        return graph

    # If a pickled graph does not exist, build a graph using the input file
    with open(edge_input_file_path) as file:
        # Build a tuple list that specifies all edges in the input file
        edge_tuple_list = []
        # Get subject and object values from each line
        for line in file:
            # Split string at tabs
            line_as_list = line.split("\t")
            subject, object = line_as_list[0], line_as_list[1]
            edge_tuple_list.append((subject, object))

        # Create graph from the 'edge_tuple_list'
        graph = igraph.Graph.TupleList(edge_tuple_list, directed=True)
        # Save graph in pickled format to the current directory
        graph.write_pickle(fname="kg2c.pickle", version=-1)
        return graph


def calculate_graph_stats(graph):
    """
    :param graph: The graph built from the TSV edge input file
    """
    global results

    # "vs" --> VertexSeq: ordered sequence of all vertices
    node_count = len(graph.vs)
    # "es" --> EdgeSeq: ordered sequence of all edges
    edge_count = len(graph.es)
    density = edge_count / (node_count * (node_count - 1))

    # Store values in 'results'
    results["created_graph"]["number_of_edges"] = edge_count
    results["created_graph"]["number_of_nodes"] = node_count
    results["created_graph"]["density"] = density

    # Calculate and store degree-related stats
    calculate_degree_stats(graph)

    # Estimate the average all-pairs shortest paths distance and
    # the diameter for a given sample of nodes
    num_nodes_in_sample = 140
    rand_node_ids = generate_rand_node_ids(graph, num_nodes_in_sample)
    get_shortest_path_lengths_directed(graph, rand_node_ids)
    get_shortest_path_lengths_undirected(graph, rand_node_ids)


def generate_rand_node_ids(graph, num_nodes_in_sample):
    """
    :param graph: The graph built from the TSV edge input file
    :param num_nodes_in_sample: Number of random node IDs to generate
    :return node_ids: A list of randomly generated node IDs
    """
    node_ids = []
    node_count = len(graph.vs)  # Number of nodes in the graph
    for _ in range(num_nodes_in_sample):
        # Generate a random node ID
        node_id = random.randint(0, node_count)
        node_ids.append(node_id)
    return node_ids


def get_shortest_path_lengths_directed(graph, rand_node_ids):
    """
    Estimate the average all-pairs shortest paths distance and the diameter
    for a given sample of nodes, specified in 'rand_node_ids'. The graph is
    treated as directed for the calculations.

    :param graph: The graph built from the TSV edge input file
    :param rand_node_ids: A list of randomly generated node IDs
    """
    global results

    # Each runtime represents the time it takes to calculate the average
    # shortest path length and diameter for one node
    runtimes = []
    avg_shortest_path_lengths = []
    diameter = float("-inf")  # To be maximized
    # Number of nodes with an average shortest path length of 0
    sink_node_count = 0

    # Find the shortest path lengths from each node specified in
    # 'rand_node_ids' to all other nodes in the graph
    for node_id in rand_node_ids:
        begin_time = datetime.datetime.now()
        # Use only outgoing shortest paths for the calculation
        matrix = graph.shortest_paths(source=[node_id], target=None,
                                      weights=None, mode="out")
        # Filter out NaN and infinity values
        filtered_matrix = [len for len in matrix[0]
                           if not math.isnan(len) and not math.isinf(len)]
        avg_shortest_path_len = np.mean(filtered_matrix)
        # Update the diameter if needed
        local_diameter = max(filtered_matrix)
        if local_diameter > diameter:
            diameter = local_diameter

        runtime = (datetime.datetime.now() - begin_time).total_seconds()
        runtimes.append(runtime)

        # If the node with 'node_id' is a sink node, do not store its
        # average shortest path length in 'avg_shortest_path_lengths'
        if avg_shortest_path_len == 0.0:
            sink_node_count += 1
            continue

        avg_shortest_path_lengths.append(avg_shortest_path_len)

    avg_runtime = sum(runtimes) / len(runtimes)
    avg_of_avg_shortest_path_lengths = (sum(avg_shortest_path_lengths) /
                                        len(avg_shortest_path_lengths))

    # Store calculations and runtime in 'results'
    results["created_graph"]["graph_as_directed"] = {}

    results["created_graph"]["graph_as_directed"]\
           ["number_of_nodes_in_sample"]\
            = len(rand_node_ids)

    results["created_graph"]["graph_as_directed"]\
           ["estimated_average_all_pairs_shortest_paths_distance_in_sample"]\
            = avg_of_avg_shortest_path_lengths

    results["created_graph"]["graph_as_directed"]\
           ["estimated_diameter_in_sample"]\
            = diameter

    results["created_graph"]["graph_as_directed"]\
           ["number_of_sink_nodes_in_sample"]\
            = sink_node_count

    results["runtimes"]\
           ["estimate_average_all_pairs_shortest_paths_distance_in_sample_for_directed_graph"]\
            = avg_runtime


def get_shortest_path_lengths_undirected(graph, rand_node_ids):
    """
    Estimate the average all-pairs shortest paths distance and the diameter
    for a given sample of nodes, specified in 'rand_node_ids'. The graph is
    treated as undirected for the calculations.

    :param graph: The graph built from the TSV edge input file
    :param rand_node_ids: A list of randomly generated node IDs
    """
    global results

    # Each runtime represents the time it takes to calculate the average
    # shortest path length and diameter for one node
    runtimes = []
    avg_shortest_path_lengths = []
    diameter = float("-inf")  # To be maximized
    # Number of nodes with an average shortest path length of 0
    sink_node_count = 0

    # Find the shortest path lengths from each node specified in
    # 'rand_node_ids' to all other nodes in the graph
    for node_id in rand_node_ids:
        begin_time = datetime.datetime.now()
        # Treat the graph as undirected for the calculation
        matrix = graph.shortest_paths(source=[node_id], target=None,
                                      weights=None, mode="all")
        # Filter out NaN and infinity values
        filtered_matrix = [len for len in matrix[0]
                           if not math.isnan(len) and not math.isinf(len)]
        avg_shortest_path_len = np.mean(filtered_matrix)
        # Update the diameter if needed
        local_diameter = max(filtered_matrix)
        if local_diameter > diameter:
            diameter = local_diameter

        runtime = (datetime.datetime.now() - begin_time).total_seconds()
        runtimes.append(runtime)

        # If the node with 'node_id' is a sink node, do not store its
        # average shortest path length in 'avg_shortest_path_lengths'
        if avg_shortest_path_len == 0.0:
            sink_node_count += 1
            continue

        avg_shortest_path_lengths.append(avg_shortest_path_len)

    avg_runtime = sum(runtimes) / len(runtimes)
    avg_of_avg_shortest_path_lengths = (sum(avg_shortest_path_lengths) /
                                        len(avg_shortest_path_lengths))

    # Store calculations and runtime in 'results'
    results["created_graph"]["graph_as_undirected"] = {}

    results["created_graph"]["graph_as_undirected"]\
           ["number_of_nodes_in_sample"]\
            = len(rand_node_ids)

    results["created_graph"]["graph_as_undirected"]\
           ["estimated_average_all_pairs_shortest_paths_distance_in_sample"]\
            = avg_of_avg_shortest_path_lengths

    results["created_graph"]["graph_as_undirected"]\
           ["estimated_diameter_in_sample"]\
            = diameter

    results["created_graph"]["graph_as_undirected"]\
           ["number_of_sink_nodes_in_sample"]\
            = sink_node_count

    results["runtimes"]\
           ["estimate_average_all_pairs_shortest_paths_distance_in_sample_for_undirected_graph"]\
            = avg_runtime


def plot_log_log_degree_distr(graph):
    """
    Generate a log-log plot of the degree distribution for the given graph.
    A PNG image of the plot will be created in the same directory as this
    script.

    :param graph: The graph built from the TSV edge input file
    Source: https://github.com/ramseylab/csx46/blob/master/class03_degdist_python3.ipynb
    """
    xs, ys = zip(*[(left, count) for left, _, count in graph.degree_distribution().bins()])
    plt.loglog(xs, ys, ".")
    plt.xlabel("Log k")  # k --> degree
    plt.ylabel("Log N")  # N --> number of nodes
    plt.savefig("log_log_degree_distr_tsv.png", bbox_inches = "tight")
    plt.show()
    plt.draw()


def calculate_degree_stats(graph):
    """
    Calculate and store degree-related stats for the given graph.

    :param graph: The graph built from the TSV edge input file
    Source: Some code was adapted from:
    https://towardsdatascience.com/visualising-graph-data-with-python-igraph-b3cc81a495cf
    """
    global results

    # Get the degree of each node in the graph
    degrees = {}
    sum_of_degrees = 0
    for node in graph.vs:
        node_id = node["name"]
        # Find adjacent nodes (both predecessors and successors) to the
        # node with 'node_id'
        neighbors = graph.neighbors(node_id, mode="all")
        degrees[node_id] = len(neighbors)
        sum_of_degrees += len(neighbors)
    
    # Calculate and store the average degree
    node_count = len(graph.vs)
    avg_degree = sum_of_degrees / node_count
    results["created_graph"]["average_degree"] = avg_degree

    # Calculate and store the maximum degree
    max_key = max(degrees, key = degrees.get)
    max_degree = degrees[max_key]
    results["created_graph"]["maximum_degree"] = max_degree
    results["created_graph"]["node_id_with_maximum_degree"] = max_key

    # Find the degree distribution and store related stats
    degree_counts = [0 for x in range(max_degree + 1)]
    for degree in degrees.values():
        degree_counts[degree] += 1
    degree_w_most_nodes = degree_counts.index(max(degree_counts))

    results["created_graph"]["degree_with_most_nodes"] = degree_w_most_nodes
    results["created_graph"]["number_of_nodes_with_most_frequent_degree"] = \
        max(degree_counts)


def main():

    global results

    # Get arguments that were passed into the script
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv_edge_input_file", type=str,
                        help="path to the Knowledge Graph TSV edge input file")
    parser.add_argument("tsv_node_input_file", type=str,
                        help="path to the Knowledge Graph TSV node input file")
    parser.add_argument("output_file_location", type=str,
                        help="path to the directory where the report file \
                        will be generated")
    arguments = parser.parse_args()
    input_file_paths = []
    input_file_paths.append(arguments.tsv_edge_input_file)
    input_file_paths.append(arguments.tsv_node_input_file)
    output_file_location = arguments.output_file_location
    output_file_path = build_output_file_path(output_file_location)

    # Get the current local date and time
    main_begin_time = datetime.datetime.now()
    datetime_str = main_begin_time.strftime("%Y-%m-%d %H:%M:%S")

    initialize_results_dict(input_file_paths, datetime_str)

    # Count the number of edges and nodes in the input files
    tsv_edge_count = get_tsv_edge_count(arguments.tsv_edge_input_file)
    tsv_node_count = get_tsv_node_count(arguments.tsv_node_input_file)
    results["input_files"]["number_of_edges"] = tsv_edge_count
    results["input_files"]["number_of_nodes"] = tsv_node_count

    # Build graph using the TSV edge input file
    begin_time = datetime.datetime.now()
    graph = build_graph(arguments.tsv_edge_input_file)
    runtime = datetime.datetime.now() - begin_time
    # Add runtime for building the graph to 'results'
    results["runtimes"]["build_graph"] = str(runtime)

    # Calculate some stats for the built graph
    begin_time = datetime.datetime.now()
    calculate_graph_stats(graph)
    runtime = datetime.datetime.now() - begin_time
    # Add runtime to 'results'
    results["runtimes"]["calculate_graph_stats"] = str(runtime)

    # Generate a log-log plot of the degree distribution
    plot_log_log_degree_distr(graph)

    # Add approximate runtime of main() to 'results'
    runtime = datetime.datetime.now() - main_begin_time
    results["runtimes"]["execute_complete_script"] = str(runtime)

    # Write the contents of 'results' to a report file
    with open(output_file_path, "w") as file:
        json.dump(results, file, indent=4)


if __name__ == "__main__":
    main()

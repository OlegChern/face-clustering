import numpy as np
import networkx as nx

from random import shuffle
from sklearn.cluster import KMeans, DBSCAN, MeanShift
from src.clustering.utils import find_euclidean_distance, find_cosine_similarity, find_taxicab_distance


def cluster_kmeans(vectors, params_dict=None):
    if params_dict is None:
        params_dict = {"clusters": 4, "random_state": 170}

    evaluator = KMeans(n_clusters=params_dict["clusters"], random_state=params_dict["random_state"])

    return evaluator.fit_predict(vectors)


def cluster_dbscan(vectors, params_dict=None):
    if params_dict is None:
        params_dict = {"eps": 1, "min_samples": 1, "metric": find_euclidean_distance}

    evaluator = DBSCAN(eps=params_dict["eps"], min_samples=params_dict["min_samples"], metric=params_dict["metric"])

    return evaluator.fit_predict(vectors)


def cluster_mean_shift(vectors, params_dict=None):
    if params_dict is None:
        params_dict = {"bandwidth": 6.3}

    evaluator = MeanShift(bandwidth=params_dict["bandwidth"])

    return evaluator.fit_predict(vectors)


def cluster_threshold(vectors, params_dict):
    if params_dict is None:
        params_dict = {"threshold": 0.15}

    labels = []
    clusters = {}
    threshold = params_dict["threshold"]
    latest_cluster = 0

    for vector in vectors:
        added = False
        for cluster in clusters.keys():
            for labeled in clusters[cluster]:
                if find_euclidean_distance(vector, labeled) <= threshold:
                    labels.append(cluster)
                    clusters[cluster].append(vector)
                    added = True
                    break

            if added:
                break
        else:
            clusters.update({latest_cluster: [vector]})
            labels.append(latest_cluster)
            latest_cluster += 1

    return labels


# https://github.com/zhly0/facenet-face-cluster-chinese-whispers-/
def chinese_whisperers(encodings, params_dict=None):
    if params_dict is None:
        params_dict = {"threshold": 0.18, "iterations": 5, "distance": find_cosine_similarity}

    threshold = params_dict["threshold"]
    iterations = params_dict["iterations"]
    distance_func = params_dict["distance"]

    nodes = []
    edges = []

    indices = range(0, len(encodings))
    for idx, face_encoding_to_check in enumerate(encodings):
        node_id = idx + 1

        node = (node_id, {'cluster': indices[idx], 'path': indices[idx]})
        nodes.append(node)

        if (idx + 1) >= len(encodings):
            break

        compare_encodings = encodings[idx + 1:]
        distances = distance_func(face_encoding_to_check, compare_encodings)
        encoding_edges = []
        for i, distance in enumerate(distances):
            if distance < threshold:
                edge_id = idx + i + 2
                encoding_edges.append((node_id, edge_id, {'weight': distance}))

        edges = edges + encoding_edges

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    for _ in range(0, iterations):
        cluster_nodes = graph.nodes()
        shuffle(np.array(cluster_nodes))
        for node in cluster_nodes:
            neighbors = graph[node]
            clusters = {}

            for ne in neighbors:
                if isinstance(ne, int):
                    if graph.nodes[ne]['cluster'] in clusters:
                        clusters[graph.nodes[ne]['cluster']] += graph[node][ne]['weight']
                    else:
                        clusters[graph.nodes[ne]['cluster']] = graph[node][ne]['weight']

            edge_weight_sum = 0
            max_cluster = 0
            for cluster in clusters:
                if clusters[cluster] > edge_weight_sum:
                    edge_weight_sum = clusters[cluster]
                    max_cluster = cluster

            graph.nodes[node]['cluster'] = max_cluster

    clusters = [0 for _ in range(len(encodings))]

    for (_, data) in graph.nodes.items():
        cluster = data['cluster']
        path = data['path']

        clusters[path] = cluster

    return clusters



import numpy as np
from sklearn.cluster import KMeans


# An abstract class for future implementations of face clustering logic
class ImageClusterer:
    Paths = []
    Vectors = []

    def __init__(self, embedding_path):
        with open(embedding_path, "r") as embeddings:
            for line in embeddings.readlines():
                path, vector_str = line.split("\t")
                vector = np.fromstring(vector_str, dtype="float32", sep=" ")

                self.Paths.append(path)
                self.Vectors.append(vector)

    def cluster_images(self, params_dict):
        pass


class KmeansClusterer(ImageClusterer):

    def cluster_images(self, params_dict=None):
        if params_dict is None:
            params_dict = {"clusters": 5, "random_state": 170}

        evaluator = KMeans(n_clusters=params_dict["clusters"], random_state=params_dict["random_state"])
        vectors = np.asarray(self.Vectors)
        labels = evaluator.fit_predict(vectors)

        return zip(self.Paths, labels)
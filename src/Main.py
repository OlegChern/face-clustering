from src.ImageLoader import ImageLoaderFaceNet
from src.EmbeddingCreator import FaceNetEmbedder
from src.ImageClusterer import KmeansClusterer

import os

# image_path = os.path.join("C:\\Users", "Olegator", "Desktop", "reunion")
# save_path = "C:\\Users\\Olegator\\Desktop\\Course Work\\Face-Clustering-Test-System\\results"
#
# loader = ImageLoaderMTCNN(image_path)
# test = loader.next_image().__next__()
# print(test)
# extractor = FaceExtractorMTCNN()
#
# extractor.extract_faces(loader, save_path)

test_file = "./embeddings/test.txt"
# model_path = "./models/facenet_keras.h5"
# faces_path = "./results"
#
# embedder = FaceNetEmbedder(model_path)
# loader = ImageLoaderFaceNet(faces_path)
#
# embedder.create_embeddings(loader, test_file)

cluster_test = KmeansClusterer(test_file)
print(cluster_test.cluster_images())
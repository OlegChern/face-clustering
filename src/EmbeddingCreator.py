from tensorflow import keras
from numpy import asarray, expand_dims


# An interface for future implementations of face embedding logic
class EmbeddingCreator:
    def create_embeddings(self, loader, save_path):
        pass


class FaceNetEmbedder(EmbeddingCreator):
    Model = None

    def __init__(self, model_path):
        self.Model = keras.models.load_model(model_path)

    def create_embeddings(self, loader, save_path):
        save_path = save_path.replace("\\", "/")

        with open(save_path, "w") as file:
            for image, image_name in loader.next_image():
                pixels = asarray(image)
                pixels = pixels.astype('float32')

                mean, std = pixels.mean(), pixels.std()
                pixels = (pixels - mean) / std

                samples = expand_dims(pixels, axis=0)
                result = self.Model.predict(samples)

                embedding = result[0]
                result_string = f"{image_name}\t{embedding}\n"
                file.write(result_string)
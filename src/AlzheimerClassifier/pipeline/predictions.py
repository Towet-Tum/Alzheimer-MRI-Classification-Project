import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from AlzheimerClassifier.utils.common import load_data, process_data
from tensorflow.keras.preprocessing.image import load_img


class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def makePrediction(self):

        model = load_model("artifacts/training/model.Xception.keras")
        img = image.load_img(self.filename, target_size=(224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        result = model.predict(img)
        clas = np.argmax(result)
        conf = result[0][clas]
        label_names = {
            "Mild Demented": 0,
            "Moderate Demented": 1,
            "Non Demented": 2,
            "Very Mild Demented": 3,
        }
        print(f"The label name ==== {label_names}")
        dict_class = dict(zip(list(range(len(label_names))), label_names))
        name = dict_class[clas]
        print(f"Label name ::: {label_names}")
        print(f"the Dictrionary:::: {dict_class}")
        print(f"The class name ::: {clas}")
        return name, conf


if __name__ == "__main__":
    img = "artifacts/data_ingestion/dataset/OriginalDataset/ModerateDemented/27.jpg"

    pred = PredictionPipeline(img)
    name, result = pred.makePrediction()
    print(f"The class:: {name}")
    print(f"The confidence:: {result}")

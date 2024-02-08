import os
from box.exceptions import BoxValueError
import yaml
from AlzheimerClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, "wb") as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())


def load_data(data_dir):

    filepaths = []
    labels = []

    # Mapping dictionary for class names
    class_mapping = {
        "MildDemented": "Mild Demented",
        "ModerateDemented": "Moderate Demented",
        "NonDemented": "Non Demented",
        "VeryMildDemented": "Very Mild Demented",
    }

    # Iterate over each class in the dataset
    for class_name, mapped_name in class_mapping.items():
        class_path = os.path.join(data_dir, class_name)

        # Check if it's a directory
        if os.path.isdir(class_path):
            filelist = os.listdir(class_path)

            # Iterate over each file in the current class
            for file in filelist:
                file_path = os.path.join(class_path, file)
                filepaths.append(file_path)
                labels.append(mapped_name)

    # Create DataFrame
    df = pd.DataFrame({"filepaths": filepaths, "labels": labels})
    return df


def process_data(df):

    labels = df["labels"]
    train_df, temp_df = train_test_split(
        df, train_size=0.8, shuffle=True, random_state=123, stratify=labels
    )
    valid_df, test_df = train_test_split(
        temp_df,
        train_size=0.5,
        shuffle=True,
        random_state=123,
        stratify=temp_df["labels"],
    )

    batch_size = 32
    img_size = (224, 224)
    channels = 3
    img_shape = (img_size[0], img_size[1], channels)

    # Create ImageDataGenerator  for training and testing
    tr_gen = ImageDataGenerator()
    ts_gen = ImageDataGenerator()

    # Training data generator
    train_gen = tr_gen.flow_from_dataframe(
        train_df,
        x_col="filepaths",
        y_col="labels",
        target_size=img_size,
        class_mode="categorical",
        color_mode="rgb",
        shuffle=True,
        batch_size=batch_size,
    )

    # Validation data generator
    valid_gen = ts_gen.flow_from_dataframe(
        valid_df,
        x_col="filepaths",
        y_col="labels",
        target_size=img_size,
        class_mode="categorical",
        color_mode="rgb",
        shuffle=True,
        batch_size=batch_size,
    )

    # Testing data generator
    test_gen = ts_gen.flow_from_dataframe(
        test_df,
        x_col="filepaths",
        y_col="labels",
        target_size=img_size,
        class_mode="categorical",
        color_mode="rgb",
        shuffle=False,
        batch_size=batch_size,
    )
    return train_gen, valid_gen, test_gen

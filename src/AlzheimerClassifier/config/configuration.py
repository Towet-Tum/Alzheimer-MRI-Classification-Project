import os
from AlzheimerClassifier.constants import *
from AlzheimerClassifier.utils.common import read_yaml, create_directories
from AlzheimerClassifier.entity.config_entity import (
    DataIngestionConfig,
    TrainingConfig,
    EvaluationConfig,
)


class ConfigurationManager:
    def __init__(
        self, config_file_path=CONFIG_FILE_PATH, params_file_path=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
        )
        return data_ingestion_config

    def get_training_config(self) -> TrainingConfig:
        config = self.config.training
        create_directories([config.root_dir])
        params = self.params
        dataset = os.path.join(
            "artifacts", "data_ingestion", "dataset", "AugmentedAlzheimerDataset"
        )
        training_config = TrainingConfig(
            root_dir=config.root_dir,
            model_path=config.model_path,
            dataset=Path(dataset),
            img_size=params.IMG_SIZE,
            epochs=params.EPOCHS,
            lr=params.LEARNING_RATE,
            weights=params.WEIGHTS,
            channels=params.CHANNELS,
            batch_size=params.BATCH_SIZE,
        )
        return training_config

    def get_evaluation_config(self) -> EvaluationConfig:

        dataset = os.path.join(
            "artifacts", "data_ingestion", "dataset", "AugmentedAlzheimerDataset"
        )
        eval_config = EvaluationConfig(
            path_of_model="artifacts/training/model.Xception.keras",
            mlflow_uri="https://dagshub.com/Towet-Tum/Alzheimer-MRI-Classification-Project.mlflow",
            all_params=self.params,
            params_image_size=self.params.IMG_SIZE,
            params_batch_size=self.params.BATCH_SIZE,
            dataset=Path(dataset),
        )
        return eval_config

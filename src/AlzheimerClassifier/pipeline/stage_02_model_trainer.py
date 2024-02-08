from AlzheimerClassifier import logger
from AlzheimerClassifier.config.configuration import ConfigurationManager
from AlzheimerClassifier.components.model_trainer import Training

STAGE_NAME = "Training Stage"


class TrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        train_config = config.get_training_config()
        trainer = Training(config=train_config)
        trainer.train()


if __name__ == "__main__":
    try:
        logger.info(f"\n\n >>>>>>>>>> The {STAGE_NAME} has started <<<<<<<<<< \n\n")
        obj = TrainingPipeline()
        obj.main()
        logger.info(
            f">>>>>>>>>>> The {STAGE_NAME} has completed succefully <<<<<<<<<< \n\n ==========="
        )
    except Exception as e:
        logger.exception(e)
        raise e

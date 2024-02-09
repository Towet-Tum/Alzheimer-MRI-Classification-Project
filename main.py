from AlzheimerClassifier import logger
from AlzheimerClassifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from AlzheimerClassifier.pipeline.stage_02_model_trainer import TrainingPipeline
from AlzheimerClassifier.pipeline.stage_03_model_evaluator import EvaluationPipeline

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f"\\n The {STAGE_NAME} has started <<<<<<<<<<<< \n\n")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(
        f">>>>>>>>>>> The {STAGE_NAME} has completed successfully <<<<<<<<<< \n\n ==========="
    )
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Training Stage"
try:
    logger.info(f"\n\n >>>>>>>>>> The {STAGE_NAME} has started <<<<<<<<<< \n\n")
    obj = TrainingPipeline()
    obj.main()
    logger.info(
        f">>>>>>>>>>> The {STAGE_NAME} has completed successfully <<<<<<<<<< \n\n ==========="
    )
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Evaluation Stage"
try:
    logger.info(f"\n\n>>>>>>>>>>>> The {STAGE_NAME} has started <<<<<<<<<<< \n\n")
    obj = EvaluationPipeline()
    obj.main()
    logger.info(
        f">>>>>>>>>>>>> The {STAGE_NAME} has completed successfully <<<<<<<<< \n\n ============="
    )
except Exception as e:
    logger.exception(e)
    raise e

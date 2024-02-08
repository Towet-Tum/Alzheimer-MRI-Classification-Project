from AlzheimerClassifier import logger
from AlzheimerClassifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f"\\n The {STAGE_NAME} has started <<<<<<<<<<<< \n\n")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(
        f">>>>>>>>>>> The {STAGE_NAME} has completed successfuly <<<<<<<<<< \n\n ==========="
    )
except Exception as e:
    logger.exception(e)
    raise e

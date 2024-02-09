from AlzheimerClassifier import logger
from AlzheimerClassifier.config.configuration import ConfigurationManager
from AlzheimerClassifier.components.model_evaluator import Evaluation

STAGE_NAME = "Evaluation Stage"


class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        eval_config = config.get_evaluation_config()
        evaluation = Evaluation(eval_config)
        evaluation.evaluation()
        evaluation.log_into_mlflow()


if __name__ == "__main__":
    try:
        logger.info(f"\n\n>>>>>>>>>>>> The {STAGE_NAME} has started <<<<<<<<<<< \n\n")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(
            f">>>>>>>>>>>>> The {STAGE_NAME} has completed succesfully <<<<<<<<< \n\n ============="
        )
    except Exception as e:
        logger.exception(e)
        raise e

from src.exception import SensorException
from src.utils import get_collection_as_dataframe
import sys,os
from src.entity import config_entity
from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation




print(__name__)
if __name__=="__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          #data ingestion
          data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          #data validation
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config,
                         data_ingestion_artifact=data_ingestion_artifact)

          data_validation_artifact = data_validation.initiate_data_validation()

          #data transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
          data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()

          #model trainer
          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact = model_trainer.initiate_model_trainer()  

          model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_eval  = ModelEvaluation(model_eval_config=model_eval_config,
           data_ingestion_artifact=data_ingestion_artifact,
           data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact)
          model_eval_artifact = model_eval.initiate_model_evaluation()


          
     except Exception as e:
          raise SensorException(e,sys)


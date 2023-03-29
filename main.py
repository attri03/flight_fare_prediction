from flight.components.data_ingestion import DataIngestion
from flight.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataCleanConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig
from flight.entity.artifact_entity import DataIngestionArtifact, DataCleanArtifact, DataTransformationArtifact, ModelTrainerArtifact
from flight.components.data_validation import DataValidation
from flight.components.data_clean import DataClean
from flight.components.data_transformation import DataTransformation
from flight.components.model_trainer import ModelTrainer
from flight.components.model_evaluator import ModelEvaluation

if __name__ == "__main__":


    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    print(data_ingestion.Initiate_Data_Ingestion())


    data_validation_config = DataValidationConfig(training_pipeline_config = training_pipeline_config)
    data_ingestion_artifact = DataIngestionArtifact(raw_file_path=data_ingestion_config.raw_data,
                                                    train_file_path=data_ingestion_config.train_data,
                                                    test_file_path=data_ingestion_config.test_data)
    data_validation = DataValidation(data_validation_config=data_validation_config,
                                     data_ingestion_artifact=data_ingestion_artifact)
    print(data_validation.Inititate_Data_Validation())


    data_clean_config = DataCleanConfig(training_pipeline_config=training_pipeline_config)
    data_clean = DataClean(data_clean_config=data_clean_config,
                           data_ingestion_artifact=data_ingestion_artifact)
    print(data_clean.Initiate_Data_Cleaning())


    data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
    data_clean_artifact = DataCleanArtifact(clean_raw_data=data_clean_config.raw_data_cleaned,
                                            clean_test_data=data_clean_config.test_data_cleaned,
                                            clean_train_data=data_clean_config.train_data_cleaned)
    data_transformation = DataTransformation(
        data_transformation_config=data_transformation_config,
        data_clean_artifact=data_clean_artifact
    )
    print(data_transformation.Initiate_Data_Transformation())


    model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
    data_transformation_artifact = DataTransformationArtifact(transformed_test_file_path=data_transformation_config.transformed_test_file,
                                                              transformer_obj=data_transformation_config.transformer_object_file_path,
                                                              transformed_train_file_path=data_transformation_config.transformed_train_file)
    model_trainer = ModelTrainer(
        model_trainer_config=model_trainer_config,
        data_transformation_artifact=data_transformation_artifact
    )
    print(model_trainer.Initiate_Model_Training())


    data_clean_artifact = DataCleanArtifact(clean_raw_data = data_clean_config.raw_data_cleaned,
                                            clean_test_data = data_clean_config.test_data_cleaned,
                                            clean_train_data = data_clean_config.train_data_cleaned)
    model_trainer_artifact = ModelTrainerArtifact(model_path = model_trainer_config.model_path)
    model_eval_config = ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
    model_evaluator = ModelEvaluation(model_eval_config = model_eval_config,
                                      data_ingestion_artifact = data_ingestion_artifact,
                                      data_transformation_artifact = data_transformation_artifact,
                                      model_trainer_artifact = model_trainer_artifact,
                                      data_clean_artifact = data_clean_artifact
                                      )
    print(model_evaluator.initiate_model_evaluation())
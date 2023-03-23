from flight.components.data_ingestion import DataIngestion
from flight.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataCleanConfig, DataTransformationConfig
from flight.entity.artifact_entity import DataIngestionArtifact, DataCleanArtifact
from flight.components.data_validation import DataValidation
from flight.components.data_clean import DataClean
from flight.components.data_transformation import DataTransformation


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
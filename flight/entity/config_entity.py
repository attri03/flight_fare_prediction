import os, sys
from flight.logger import logging
from flight.exception import CustomException
from datetime import datetime

RAW_DATA = 'raw_data.csv'
REPORT_NAME = 'report.yaml'
TRAIN_DATA = 'train_data.csv'
TEST_DATA = 'test_data.csv'
CLEANED_TRAIN_DATA = 'clean_train_data.csv'
CLEANED_TEST_DATA = 'clean_test_data.csv'
RAW_DATA_CLEANED = 'clean_raw_data.csv'
TRANSFORMER_OBJ_FILE = 'transformer_obj.pkl'
TRANSFORMED_TRAIN_FILE = 'transformed_train_file.csv'
TRANSFORMED_TEST_FILE = 'transformed_test_file.csv'
 
class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir:str = os.path.join(os.getcwd(), 'artifact', f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise CustomException(e, sys)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config : TrainingPipelineConfig):
        try:
            self.Database:str = 'flight'
            self.Collection:str = 'price'
            self.data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir, 'data_ingestion')
            self.raw_data:str = os.path.join(self.data_ingestion_dir, RAW_DATA)
            self.train_data:str = os.path.join(self.data_ingestion_dir, TRAIN_DATA)
            self.test_data:str = os.path.join(self.data_ingestion_dir, TEST_DATA)
            self.test_size:float = 0.2
        except Exception as e:
            raise CustomException(e, sys)

class DataValidationConfig:
    def __init__(self, training_pipeline_config : TrainingPipelineConfig):
        try:
            self.base_data = 'E:\Flight_Fare_Prediction\Data_Train.xlsx'
            self.data_val_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_validation')
            self.report_path = os.path.join(self.data_val_dir, REPORT_NAME)
            self.threshold_value_null:float = 30
            self.threshold_value_column:float = 70
        except Exception as e:
            raise CustomException(e, sys)

class DataCleanConfig:
    def __init__(self, training_pipeline_config : TrainingPipelineConfig):
        try:
            self.data_clean_dir:str = os.path.join(training_pipeline_config.artifact_dir, 'data_clean')
            self.train_data_cleaned:str = os.path.join(self.data_clean_dir, CLEANED_TRAIN_DATA)
            self.test_data_cleaned:str = os.path.join(self.data_clean_dir, CLEANED_TEST_DATA)
            self.raw_data_cleaned:str = os.path.join(self.data_clean_dir, RAW_DATA_CLEANED)
        except Exception as e:
            raise CustomException(e, sys)
        
class DataTransformationConfig:
    def __init__(self, training_pipeline_config : TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_transformation')
            self.transformer_object_file_path = os.path.join(self.data_transformation_dir, TRANSFORMER_OBJ_FILE)
            self.transformed_train_file = os.path.join(self.data_transformation_dir, TRANSFORMED_TRAIN_FILE)
            self.transformed_test_file = os.path.join(self.data_transformation_dir, TRANSFORMED_TEST_FILE)
        except Exception as e:
            raise CustomException(e, sys)

class ModelTrainerConfig:
    pass

class ModelEvaluationConfig:
    pass

class ModelPusherConfig:
    pass
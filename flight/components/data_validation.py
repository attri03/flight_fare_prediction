from flight.entity.config_entity import DataValidationConfig
from flight.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from flight.exception import CustomException
from flight.logger import logging
import os, sys
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from flight.utils import convert_to_yaml_file

class DataValidation:

    def __init__(
            self, data_validation_config : DataValidationConfig, 
            data_ingestion_artifact : DataIngestionArtifact
            ):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.report:dict = {}
            self.data_drift_dic:dict = {}
        except Exception as e:
            raise CustomException(e, sys)
        
    def check_null_values(self, df, report_key:str):
        try:
            logging.info('checking for columns with more than 30% null values')
            array_null_values = []
            for column in df.columns:
                percentage_of_missing_values = (df[column].isnull().sum()/len(df[column]))*100
                if percentage_of_missing_values > self.data_validation_config.threshold_value_null:
                    df = df.drop(column, axis = 1)
                    array_null_values.append(column)
            logging.info(f'columns with more than 30% null values are {array_null_values}')
            self.report[report_key] = array_null_values
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def check_columns(self, base_df, current_df, report_key):
        try:
            logging.info('checking for columns percentage in base and current dataframe')
            not_in_current_df = []
            logging.info(f'{base_df.shape}')
            for column in base_df.columns:
                if column not in current_df.columns:
                    not_in_current_df.append(column)

            logging.info(f'columns that are not in current dataframe are {not_in_current_df}')
            self.report[report_key] = not_in_current_df
            if (len(not_in_current_df)/len(base_df.columns))*100 > self.data_validation_config.threshold_value_column:
                return None
            else:
                return self.report
        except Exception as e:
            raise CustomException(e, sys)
        
    def Inititate_Data_Validation(self):

        try:
            logging.info('Lets start data validation phase')

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info('train data read')

            test_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info('test data read')

            os.makedirs(os.path.join(self.data_validation_config.data_val_dir))
            logging.info('directory made for data validation phase')

            base_df = pd.read_excel(self.data_validation_config.base_data)

            train_df = self.check_null_values(df = train_df, report_key='check_null_values_for_training_data')
            test_df = self.check_null_values(df=test_df, report_key='check_null_values_for_testing_data')

            final_report_1 = self.check_columns(base_df = base_df, 
                            current_df = train_df, report_key = 'check_columns_for_training_data')
            final_report_2 = self.check_columns(base_df = base_df, 
                            current_df = test_df, report_key = 'check_columns_for_testing_data')
            
            if final_report_1== None or final_report_2 == None:
                raise Exception('Data is not appropriate')
            else:
                logging.info('creating yaml file')
                convert_to_yaml_file(data = final_report_2, file_path = self.data_validation_config.report_path)
                logging.info('yaml file created')

            data_validation_artifact = DataValidationArtifact(
                report_file_path=self.data_validation_config.report_path
            )
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)

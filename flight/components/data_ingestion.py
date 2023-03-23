from flight.entity.config_entity import DataIngestionConfig
from flight.entity.artifact_entity import DataIngestionArtifact
from flight.exception import CustomException
import os, sys
from flight.utils import get_collection_as_dataframe
import numpy as np 
import pandas as pd
from flight.logger import logging
from sklearn.model_selection import train_test_split
 
class DataIngestion:

    def __init__(self, data_ingestion_config : DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)
        
    def Initiate_Data_Ingestion(self):
        try:

            logging.info('entering into data ingestion phase')

            df = get_collection_as_dataframe(
                Database=self.data_ingestion_config.Database, 
                collection=self.data_ingestion_config.Collection
            )
            logging.info('Data called from mongoDB successfully')

            logging.info(f'{df.shape}')

            df.replace({'na': np.nan}, inplace = True)
            logging.info('na values replaced with np.nan')

            os.makedirs(os.path.join(self.data_ingestion_config.data_ingestion_dir))
            logging.info('data ingestion directory made successfully')

            df.to_csv(self.data_ingestion_config.raw_data, index=False, header=True)
            logging.info('data saved to the directory as raw data')

            train_data, test_data = train_test_split(df, train_size = self.data_ingestion_config.test_size, random_state = 42)
            logging.info(f'train shape is {train_data.shape}, test shape is {test_data.shape}')

            train_data.to_csv(self.data_ingestion_config.train_data, index=False, header=True)
            logging.info('training data saved to the directory as train data')

            test_data.to_csv(self.data_ingestion_config.test_data, index=False, header=True)
            logging.info('testing data saved to the directory as test data')

            data_ingestion_artifact = DataIngestionArtifact(
                raw_file_path=self.data_ingestion_config.raw_data,
                train_file_path=self.data_ingestion_config.train_data,
                test_file_path=self.data_ingestion_config.test_data
            )
            logging.info('data ingestion phase completed')

            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e, sys)
        
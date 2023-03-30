from flight.config import mongo_client_url
import pandas as pd
from flight.logger import logging
from flight.exception import CustomException
import os, sys
import yaml
import numpy as np
import pickle
import dill

def get_collection_as_dataframe(Database:str, collection:str):
    try:
        df = pd.DataFrame(list(mongo_client_url[Database][collection].find()))
        logging.info('getting the data from mongodb')
        if '_id' in df.columns:
            df = df.drop('_id', axis = 1)
        logging.info('removed _id column')
        #logging.info(f'{df.shape}')
        return df
    except Exception as e:
        raise CustomException(e, sys)
    
def convert_to_yaml_file(data, file_path):
    try:
        with open(file_path, "w") as file_path:
            yaml.dump(data, file_path)
    except Exception as e:
        raise CustomException(e, sys)
    
def drop_unwanted_columns(data, columns_to_be_droped):
    try:
        logging.info('Droping unwanted columns')
        data = data.drop(columns_to_be_droped, axis = 1)
        return data
    except Exception as e:
        raise CustomException(e, sys)
    
def object_to_float(data, target_column):
    try:
        logging.info('Converting object datatype to float')
        for column in data.columns:
            if column not in target_column:
                data[column] = data[column].astype(float)
        return data
    except Exception as e:
        raise CustomException(e, sys)
    
def drop_na_values(data):
    try:
        logging.info('Dropping null values')
        data = data.dropna()
        return data
    except Exception as e:
        raise CustomException(e, sys)
    
def save_numpy_data(data, file_path):
    try:
        logging.info('saving the numpy file')
        np.save(file_path, data)
    except Exception as e:
        raise CustomException(e, sys)

def save_pickle_file(file, file_path):
    try:
        with open(file_path, 'wb') as file_path:
            pickle.dump(file, file_path)
    except Exception as e:
        raise CustomException(e, sys)
    
def load_numpy_data(path):
    try:
        logging.info('Loading the daved numpy array file')
        data = np.load(path)
        return data
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise CustomException(e, sys)
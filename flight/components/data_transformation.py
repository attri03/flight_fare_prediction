from flight.entity.config_entity import DataTransformationConfig
from flight.entity.artifact_entity import DataTransformationArtifact, DataCleanArtifact
from flight.exception import CustomException
from flight.logger import logging
import os, sys
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
from flight.utils import save_numpy_data, save_pickle_file

class DataTransformation:
    def __init__(self, 
                 data_transformation_config : DataTransformationConfig,
                 data_clean_artifact : DataCleanArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_clean_artifact = data_clean_artifact
        except Exception as e:
            raise CustomException(e, sys)
        
    def transformation_pipeline(self, numeric_columns, categoric_columns):
        try:
            pipeline1 = Pipeline(
                [
                ('scaler', StandardScaler()),
                ]
            )
            pipeline2 = Pipeline(
                [
                ('encoder', OneHotEncoder())
                ]
            )
            column_transformer = ColumnTransformer(
                [
                ('pipe1', pipeline1, numeric_columns),
                ('pipe2', pipeline2, categoric_columns)
                ]
            )
            return column_transformer
        except Exception as e:
            raise CustomException(e, sys)

    def Initiate_Data_Transformation(self):
        try:
            logging.info('Lets start our data transformation phase')

            train_df = pd.read_csv(self.data_clean_artifact.clean_train_data)
            test_df = pd.read_csv(self.data_clean_artifact.clean_test_data)
            logging.info('Imported the training and testing data')

            DEPENDENT_COLUMN = 'Price'
            x_train_df = train_df.drop(DEPENDENT_COLUMN, axis = 1)
            x_test_df = test_df.drop(DEPENDENT_COLUMN, axis = 1)
            y_train_df = train_df[DEPENDENT_COLUMN]
            y_test_df = test_df[DEPENDENT_COLUMN]
            logging.info('dependent and independent variables seperated')

            numeric_columns = [column for column in x_train_df if x_train_df[column].dtypes != 'object']
            categorical_columns = [column for column in x_train_df if x_train_df[column].dtypes == 'object']
            logging.info('Seperated the numeric and categoric columns')

            transformation_pipeline_obj = self.transformation_pipeline(numeric_columns=numeric_columns, categoric_columns=categorical_columns)
            transformation_pipeline_obj.fit(x_train_df)
            logging.info('Fitting the training data into transformation pipeline')

            transformed_x_training_data = transformation_pipeline_obj.transform(x_train_df)
            transformed_x_testing_data = transformation_pipeline_obj.transform(x_test_df)
            logging.info('transformed both training and testing x data')

            os.makedirs(os.path.join(self.data_transformation_config.data_transformation_dir))
            logging.info('Making the data transformation directory')

            train_data = np.c_[transformed_x_training_data, np.array(y_train_df)]
            test_data = np.c_[transformed_x_testing_data, np.array(y_test_df)]
            logging.info('Entire training ang testing data ready')

            save_numpy_data(data = train_data,file_path=self.data_transformation_config.transformed_train_file)
            save_numpy_data(data=test_data, file_path=self.data_transformation_config.transformed_test_file)
            logging.info('Saved both training and testing data in numpy file')

            save_pickle_file(file = transformation_pipeline_obj, file_path = self.data_transformation_config.transformer_object_file_path)
            logging.info('Pickle file created')

            data_transformation_artifact = DataTransformationArtifact(
                transformer_obj=self.data_transformation_config.transformer_object_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file
            )

            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys)


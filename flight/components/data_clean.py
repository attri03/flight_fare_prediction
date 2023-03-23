from flight.entity.config_entity import DataCleanConfig
from flight.entity.artifact_entity import DataIngestionArtifact, DataCleanArtifact
from flight.exception import CustomException
from flight.logger import logging
import os, sys
import pandas as pd
from flight.utils import drop_unwanted_columns, object_to_float, drop_na_values

class DataClean:

    def __init__(self,data_clean_config : DataCleanConfig, 
                data_ingestion_artifact : DataIngestionArtifact):
        try:
            self.data_clean_config = data_clean_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)
        
    def Initiate_Data_Cleaning(self):
        try:

            logging.info('Lets start data cleaning phase')

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            raw_df = pd.read_csv(self.data_ingestion_artifact.raw_file_path)
            logging.info('Training, testing and raw data read successfully')

            train_df['Destination'] = train_df['Destination'].replace('New Delhi', 'Delhi')
            test_df['Destination'] = test_df['Destination'].replace('New Delhi', 'Delhi')
            raw_df['Destination'] = raw_df['Destination'].replace('New Delhi', 'Delhi')

            train_df['day_of_Journey'] = train_df['Date_of_Journey'].str.split('/').str.slice(0,1).str.join('')
            train_df['month_of_Journey'] = train_df['Date_of_Journey'].str.split('/').str.slice(1,2).str.join('')
            train_df['year_of_Journey'] = train_df['Date_of_Journey'].str.split('/').str.slice(2,3).str.join('')
            test_df['day_of_Journey'] = test_df['Date_of_Journey'].str.split('/').str.slice(0,1).str.join('')
            test_df['month_of_Journey'] = test_df['Date_of_Journey'].str.split('/').str.slice(1,2).str.join('')
            test_df['year_of_Journey'] = test_df['Date_of_Journey'].str.split('/').str.slice(2,3).str.join('')
            raw_df['day_of_Journey'] = raw_df['Date_of_Journey'].str.split('/').str.slice(0,1).str.join('')
            raw_df['month_of_Journey'] = raw_df['Date_of_Journey'].str.split('/').str.slice(1,2).str.join('')
            raw_df['year_of_Journey'] = raw_df['Date_of_Journey'].str.split('/').str.slice(2,3).str.join('')

            train_df['Total_Stops'] = train_df['Total_Stops'].str.split(' ').str.slice(0,1).str.join('').replace('non-stop',0)
            test_df['Total_Stops'] = test_df['Total_Stops'].str.split(' ').str.slice(0,1).str.join('').replace('non-stop',0)
            raw_df['Total_Stops'] = raw_df['Total_Stops'].str.split(' ').str.slice(0,1).str.join('').replace('non-stop',0)

            duration = list(train_df['Duration'])
            for i in range(len(duration)):
                if len(duration[i].split()) != 2:
                    if 'h' in duration[i]:
                        duration[i] = duration[i] + ' ' + '0m'
                    else:
                        duration[i] = '0h ' + " " + duration[i]  
            duration_hour = []
            duration_minute = []
            for i in range(len(duration)):
                duration_hour.append(int(duration[i].split('h')[0]))
                duration_minute.append(int(duration[i].split('m')[0].split()[-1]))
            train_df['Duration_hour'] = duration_hour
            train_df['duration_minute'] = duration_minute
            train_df['Duration_hour'] = train_df['Duration_hour'].astype(int)
            train_df['Duration_hour'] = train_df['Duration_hour']*60
            train_df['Total_duration_in_minutes'] = train_df['Duration_hour'] + train_df['duration_minute'].astype(int)

            duration = list(test_df['Duration'])
            for i in range(len(duration)):
                if len(duration[i].split()) != 2:
                    if 'h' in duration[i]:
                        duration[i] = duration[i] + ' ' + '0m'
                    else:
                        duration[i] = '0h ' + " " + duration[i]  
            duration_hour = []
            duration_minute = []
            for i in range(len(duration)):
                duration_hour.append(int(duration[i].split('h')[0]))
                duration_minute.append(int(duration[i].split('m')[0].split()[-1]))
            test_df['Duration_hour'] = duration_hour
            test_df['duration_minute'] = duration_minute
            test_df['Duration_hour'] = test_df['Duration_hour'].astype(int)
            test_df['Duration_hour'] = test_df['Duration_hour']*60
            test_df['Total_duration_in_minutes'] = test_df['Duration_hour'] + test_df['duration_minute'].astype(int)

            duration = list(raw_df['Duration'])
            for i in range(len(duration)):
                if len(duration[i].split()) != 2:
                    if 'h' in duration[i]:
                        duration[i] = duration[i] + ' ' + '0m'
                    else:
                        duration[i] = '0h ' + " " + duration[i]  
            duration_hour = []
            duration_minute = []
            for i in range(len(duration)):
                duration_hour.append(int(duration[i].split('h')[0]))
                duration_minute.append(int(duration[i].split('m')[0].split()[-1]))
            raw_df['Duration_hour'] = duration_hour
            raw_df['duration_minute'] = duration_minute
            raw_df['Duration_hour'] = raw_df['Duration_hour'].astype(int)
            raw_df['Duration_hour'] = raw_df['Duration_hour']*60
            raw_df['Total_duration_in_minutes'] = raw_df['Duration_hour'] + raw_df['duration_minute'].astype(int)

            train_df['Arrival_time'] = train_df['Arrival_Time'].str.split(' ').str.slice(0,1).str.join('')
            train_df['Dep_Time_Hour'] = train_df['Dep_Time'].str.split(':').str.slice(0,1).str.join('')
            train_df['Dep_Time_Minute'] = train_df['Dep_Time'].str.split(':').str.slice(1,2).str.join('')
            train_df['Arrival_Time_Hour'] = train_df['Arrival_time'].str.split(':').str.slice(0,1).str.join('')
            train_df['Arrival_Time_Minute'] = train_df['Arrival_time'].str.split(':').str.slice(1,2).str.join('')

            test_df['Arrival_time'] = test_df['Arrival_Time'].str.split(' ').str.slice(0,1).str.join('')
            test_df['Dep_Time_Hour'] = test_df['Dep_Time'].str.split(':').str.slice(0,1).str.join('')
            test_df['Dep_Time_Minute'] = test_df['Dep_Time'].str.split(':').str.slice(1,2).str.join('')
            test_df['Arrival_Time_Hour'] = test_df['Arrival_time'].str.split(':').str.slice(0,1).str.join('')
            test_df['Arrival_Time_Minute'] = test_df['Arrival_time'].str.split(':').str.slice(1,2).str.join('')

            raw_df['Arrival_time'] = raw_df['Arrival_Time'].str.split(' ').str.slice(0,1).str.join('')
            raw_df['Dep_Time_Hour'] = raw_df['Dep_Time'].str.split(':').str.slice(0,1).str.join('')
            raw_df['Dep_Time_Minute'] = raw_df['Dep_Time'].str.split(':').str.slice(1,2).str.join('')
            raw_df['Arrival_Time_Hour'] = raw_df['Arrival_time'].str.split(':').str.slice(0,1).str.join('')
            raw_df['Arrival_Time_Minute'] = raw_df['Arrival_time'].str.split(':').str.slice(1,2).str.join('')

            train_df = drop_na_values(train_df)
            test_df = drop_na_values(test_df)
            raw_df = drop_na_values(raw_df)
            logging.info('Dropped all nan values')

            columns_to_be_droped = ['Date_of_Journey','Route', 'Duration_hour','duration_minute','Duration', 'Arrival_Time', 'Dep_Time', 'Arrival_time', 'Additional_Info']
            train_df = drop_unwanted_columns(data = train_df, columns_to_be_droped = columns_to_be_droped)
            test_df = drop_unwanted_columns(data = test_df, columns_to_be_droped = columns_to_be_droped)
            raw_df = drop_unwanted_columns(data = raw_df, columns_to_be_droped = columns_to_be_droped)
            logging.info('Dropped all unwanted columns')

            TARGET_COLUMN = ['Airline', 'Source', 'Destination']
            train_df = object_to_float(data = train_df, target_column=TARGET_COLUMN)
            test_df = object_to_float(data = test_df, target_column=TARGET_COLUMN)
            raw_df = object_to_float(data = raw_df, target_column=TARGET_COLUMN)
            logging.info('Converted datatypes from object to float')

            logging.info(f'{train_df.dtypes}, {test_df.dtypes}, {raw_df.dtypes}')

            os.makedirs(os.path.join(self.data_clean_config.data_clean_dir))
            logging.info('Making the data_clean directory')

            train_df.to_csv(self.data_clean_config.train_data_cleaned, index=False, header=True)
            test_df.to_csv(self.data_clean_config.test_data_cleaned, index=False, header=True)
            raw_df.to_csv(self.data_clean_config.raw_data_cleaned, index=False, header=True)
            logging.info('Training and testing data saved')

            data_clean_artifact = DataCleanArtifact(
                clean_test_data=self.data_clean_config.test_data_cleaned,
                clean_train_data=self.data_clean_config.train_data_cleaned,
                clean_raw_data=self.data_clean_config.raw_data_cleaned
            )
            logging.info('data cleaning phase completed')
            return data_clean_artifact

        except Exception as e:
            raise CustomException(e, sys)

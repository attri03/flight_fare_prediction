from flight.logger import logging
from flight.exception import CustomException
from flight.entity.config_entity import ModelTrainerConfig
from flight.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
import os, sys
from flight.utils import load_numpy_data, save_pickle_file
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

class ModelTrainer:

    def __init__(self, 
                 model_trainer_config : ModelTrainerConfig,
                 data_transformation_artifact : DataTransformationArtifact
                 ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            self.score_dict = {}
            self.model_dic = {}
        except Exception as e:
            raise CustomException(e, sys)
        
    def Finding_the_best_model(self, model_dict, x_training_data, y_training_data, x_testing_data, y_testing_data):
        try:
            for i in range(0,len(list(model_dict.items()))):
                model = list(model_dict.items())[i][1]
                logging.info(f'training the data on : {model} model')
                model.fit(x_training_data, y_training_data)
                y_pred = model.predict(x_testing_data)
                r2_Score = r2_score(y_true = y_testing_data, y_pred = y_pred)
                logging.info(f'Accuracy for {model} model is : {r2_Score}')
                self.score_dict[list(model_dict.items())[i][0]] = r2_Score
                self.model_dic[list(model_dict.items())[i][0]] = model
            max_key = max(zip(self.score_dict.values(), self.score_dict.keys()))[1]
            best_model = self.model_dic[max_key]
            return best_model
        except Exception as e:
            raise CustomException(e, sys)
        
    def Initiate_Model_Training(self):
        try:

            logging.info('Lets start our Model Training part')

            train_arr = load_numpy_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_data(self.data_transformation_artifact.transformed_test_file_path)
            logging.info('Loaded both training and testing array')

            x_train_arr = train_arr[:,:-1]
            y_train_arr = train_arr[:,-1]
            x_test_arr = test_arr[:,:-1]
            y_test_arr = test_arr[:,-1]
            logging.info(f'dependent training data is : {x_train_arr.shape}, independent training data is : {y_train_arr.shape}')
            logging.info(f'dependent testing data is : {x_test_arr.shape}, independent testing data is : {y_test_arr.shape}')

            model_dict = {
                'AdaBoost_Regressor' : AdaBoostRegressor(),
                'RandomForest_Regressor' : RandomForestRegressor(),
                'DecisionTree_Regressor' : DecisionTreeRegressor(),
                'XGB_Regressor' : XGBRegressor()
            }

            best_model = self.Finding_the_best_model(model_dict=model_dict,  
                             x_training_data=x_train_arr,
                             y_training_data=y_train_arr,
                             x_testing_data=x_test_arr,
                             y_testing_data=y_test_arr
                             )
            logging.info('Best model found')

            y_pred_train = best_model.predict(x_train_arr)
            y_pred_test = best_model.predict(x_test_arr)
            r2_score_train = r2_score(y_true = y_train_arr, y_pred = y_pred_train)
            r2_score_test = r2_score(y_true = y_test_arr, y_pred = y_pred_test)
            logging.info('r2_score found for both training and testing data')

            difference = abs(r2_score_train - r2_score_test)

            if r2_score_train < self.model_trainer_config.threshold_value:
                raise Exception('Model has very less accuracy')

            if difference < 0.1:
                raise Exception('Model is overfitted')
            logging.info('Checked for model accuracy and overfitting criterion')
            
            os.makedirs(os.path.join(self.model_trainer_config.model_train_dir))
            logging.info('Model training directory made')

            save_pickle_file(file = best_model, file_path=self.model_trainer_config.model_path)
            logging.info('pickle file created for the model')

            model_trainer_artifact = ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path
            )

            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)
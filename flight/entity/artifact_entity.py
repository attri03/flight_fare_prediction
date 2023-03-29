from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    raw_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataCleanArtifact:
    clean_train_data:str
    clean_test_data:str
    clean_raw_data:str

@dataclass
class DataTransformationArtifact:
    transformer_obj:str
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float

@dataclass
class ModelPusherArtifact:
    pass
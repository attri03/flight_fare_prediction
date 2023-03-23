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
    pass

@dataclass
class ModelTrainerArtifact:
    pass

@dataclass
class ModelEvaluationArtifact:
    pass

@dataclass
class ModelPusherArtifact:
    pass
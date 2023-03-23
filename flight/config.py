import pymongo
import os
class EnvironmentVariables:
    def __init__(self):
        self.mongo_client:str = os.getenv('MONGO_DB_URL')

environment_variable = EnvironmentVariables()
mongo_client_url = pymongo.MongoClient(environment_variable.mongo_client)


import pandas as pd
import numpy as np
from flight.config import mongo_client_url
import json

data_path = 'E:\Flight_Fare_Prediction\Data_Train.xlsx'
Database_name = 'flight'
collection_name = 'price'
if __name__ == '__main__':
    df = pd.read_excel(data_path)
    df.reset_index(drop=True,inplace=True)
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    mongo_client_url[Database_name][collection_name].insert_many(json_record)


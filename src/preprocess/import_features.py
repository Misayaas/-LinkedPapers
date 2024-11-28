import pandas as pd
import os
import sys
import os.path as path
cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/../..")

from sqlalchemy import column

from src import create_app
from src.models import Paper, create_session, Citation, Feature, create_tables
from sqlalchemy.orm import sessionmaker
from pymilvus import MilvusClient
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection

# 建立连接

def import_papers(csv_path):

    client = MilvusClient("feat.db")
    if client.has_collection(collection_name="feat"):
        client.drop_collection(collection_name="feat")

    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=False
    )

    DIM = 128

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True),
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=DIM),

    client.create_collection(
        collection_name="feat",
        dimension=128,  # The vectors we will use in this demo has 128 dimensions
        schema=schema,
    )

    feats = pd.read_csv(path.join(csv_path, 'feats.csv.gz'), compression='gzip')

    paper_id = 1

    client.load_collection("feat")
    for _, row in feats.iterrows():
        feat = {"id": paper_id,  "vector": [row [col] for col in feats.columns]}
        client.insert("feat", feat)
        if (paper_id+1)%1000 == 0:
            print('committed', paper_id)
        paper_id += 1

    index_params = client.prepare_index_params()
 
    # 3.4. Add indexes
    index_params.add_index(
        field_name="id"
    )
     
    index_params.add_index(
        field_name="vector", 
        index_type="AUTOINDEX",
        metric_type="IP"
    )

    client.create_index("feat", index_params)


if __name__ == "__main__":
    import_papers('~/Projects/BigData/hw3')

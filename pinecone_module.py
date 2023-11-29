import pinecone # to interact with Pinecone
from sqlite_module import * # to interact with SQLite database.
import os # to access environment variables
import json # to deserialize the vector from SQLite database

def pinecone_init(index_name: str = 'socialvegan'):
    '''initialize connection to Pinecone (get API key at app.pinecone.io)'''
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment="us-east1-gcp"
    )
    # check if index already exists (it shouldn't if this is first time)
    if index_name not in pinecone.list_indexes():
        # if does not exist, create index
        pinecone.create_index(
            index_name,
            dimension=1536,
            metric='cosine',
            metadata_config={'indexed': ['channel_id', 'published']} # useless code, guess why im not deleting this yet?
        )
    # connect to index
    index = pinecone.Index(index_name)
    return index

def pinecone_vector_upsert(person_id, index):
    '''extract the vector of a person from SQLite database and upsert it into pinecone index'''
    vector = json.loads(db_data_read(person_id, 'vector', 'user.db'))
    age = db_data_read(person_id, 'age', 'user.db')
    man = db_data_read(person_id, 'man', 'user.db')
    hetero = db_data_read(person_id, 'hetero', 'user.db')
    city = db_data_read(person_id, 'city', 'user.db')
    
    index.upsert(
        vectors = [{
            'id': person_id,
            'values': vector,
            'metadata': {'age': age,'man':man,'hetero': hetero, 'city':city}
        }]
    )

def pinecone_fetch(personid, index):
    '''fetch the vector of a person in pinecone index'''
    return index.fetch([personid])

def pinecone_delete(personid, index) -> None:
    '''delete the vector of a person in pinecone index'''
    index.delete([personid])

def pinecone_query(index, personid, k) -> None:
    '''query the pinecone index for k nearest neighbors of a person'''
    hetero = db_data_read(personid, 'hetero', 'user.db')
    vector = json.loads(db_data_read(personid, 'vector', 'user.db'))
    man = db_data_read(personid, 'man', 'user.db')
    
    if hetero == True:
        qresult = index.query(
            vector = vector,
            filter = {
                "man": {"$ne": man},
            },
            top_k = k,
            include_metadata = True
        )

    elif hetero == False:
        qresult = index.query(
            vector = vector,
            filter = {
                "man": {"$eq": man}
            },
            top_k = k,
            include_metadata = True
        )
        
    # result = [[id1, score1], [id2, score2], ...]
    for i in qresult["matches"]:
        db_data_update(json.dumps([i["id"],i["score"]]), "match_result_id", personid, "user.db")
        
    return None


def pinecone_delete_index(index_name: str):
    '''delete the pinecone index'''
    pinecone.delete_index(index_name)
    print("Deleted index successfully")
    return


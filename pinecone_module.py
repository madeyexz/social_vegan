import pinecone
from sqlite_module import * # to interact with SQLite database.
import os

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
    '''create the vector of a person in pinecone index'''
    
    
    index.upsert(
        vectors = [{
            'id': person.id,
            'values': person.vector,
            'metadata': {'age': person.age,'man':person.man,'hetero': person.hetero, 'city':person.city}
        }]
    )

def pinecone_fetch(person, index):
    '''fetch the vector of a person in pinecone index'''
    return index.fetch([person.id])

def pinecone_delete(person, index):
    '''delete the vector of a person in pinecone index'''
    index.delete([person.id])

def pinecone_query(index, person, k):
    '''query the pinecone index for k nearest neighbors of a person'''
    if person.hetero == True:
        qresult = index.query(
            vector=person.vector,
            filter={
                "man": {"$ne": person.man},
            },
            top_k = k,
            include_metadata = True
        )
    elif person.hetero == False:
        qresult = index.query(
            vector=person.vector,
            filter={
                "man": {"$eq": person.man}
            },
            top_k = k,
            include_metadata = True
        )
    result = []
    # result = [[id1, score1], [id2, score2], ...]
    for i in qresult["matches"]:
        result.append([i["id"],i["score"]])
        
    return result

def pinecone_delete_index(index_name: str):
    '''delete the pinecone index'''
    pinecone.delete_index(index_name)
    print("Deleted index successfully")
    return


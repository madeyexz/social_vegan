from person_class import Person
from pinecone_module import *
from json_local_db import *
from chatbot_module import *

def main():

    # preset_data = [["lara",18,False,True,"BJ","A@gmail.com","I am a stone"],["lance",19,True,True,"BJ","B@gmail.com","I am a cat"],["jimmy",25,True,True,"BJ","C@gmail.com","I am a kitten"]]
    # # initialize the database
    # db_reset('user.db')
    # # format the data
    # for i in preset_data:
    #     db_data_insert(Person(i[0],i[1],i[2],i[3],i[4],i[5],i[6]).to_dict(),'user.db')
    
    # get all ids
    ids = db_get_all_ids('user.db')
    
    # # initialize the pinecone index
    # index = pinecone_init('socialvegan')
    
    # # insert the vectors into pinecone index
    # for i in ids:
    #     pinecone_vector_upsert(i, index)
    #     print(f"Inserted {i} into pinecone successfully")
    
    # # for every entry, query its k nearest neighbors
    # for i in ids:
    #     pinecone_query(index, i, 3)
    #     print(f"Queried {i} in pinecone successfully")
    
    # # print the results without vector col
    # db_print_without_vector('user.db')
    
    # getting the final results
    user_id = ids[0]
    database_path = 'user.db'
    user_name = db_data_read(user_id, 'name', database_path)
    user_exp = db_data_read(user_id, 'expectation', database_path)
    user_match_result =  json.loads(db_data_read(user_id,'match_result_id', database_path)) # matched id and score, enclosed in list
    for i in user_match_result:
        matched_id, matched_score = i[0], i[1]
        if user_id == matched_id:
            continue
        else:
            matched_name, matched_exp = db_data_read(matched_id, 'name', database_path), db_data_read(matched_id, 'expectation', database_path)
            prompt = f"My expectation is '{user_exp}', and his/her expectation is '{matched_exp}'. Why are we a good match?"
            result = chatbot_completion(prompt)
        
        print(f"You ({user_name}) are matched with {matched_name} with a score of {matched_score}!")
        print(f"Your expectation is: {user_exp}")
        print(f"{matched_name}'s expectation is: {matched_exp}")
        print(result)
        print()
        print()
        

if __name__ == '__main__':
    # test()
    main()
from person_class import Person
from pinecone_deployment import *
from json_local_db import *

def main():

    pinecone_index = pinecone_init()
    # print(pinecone_index.describe_index_stats())
    
    # a 2d list of id-Person pair, where id = name + email
    # for each entry in the list, create a person object and upsert the vector into pinecone index
    
    '''ADDING USER INFORMATION'''
    preset_data = [["lara",18,False,True,"BJ","A@gmail.com","I am a stone"],["lance",19,True,True,"BJ","B@gmail.com","I am a cat"],["jimmy",25,True,True,"BJ","C@gmail.com","I am a kitten"]]
    
    db = [] # database
    for i in preset_data:
        try:
            db.append(Person(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
        except ValueError as e:
            print(f"Error: {e}")
            '''API COMMUNICATIONS HERE'''
    
    print(db)
    '''usr input'''
    '''for each new user input, create a new Person object, add it into db[]'''
    
    with open("data.txt", "w") as f:
        f.write(str(pinecone_fetch(db[0], pinecone_index)))
    
    for i in db:
        pinecone_vector_upsert(i, pinecone_index)
    
    print(pinecone_index.describe_index_stats())
    
    '''QUERYING'''
    qperson = db[0]
    qresult = pinecone_query(pinecone_index, qperson, 3)
    
    '''PRINTING RESULTS'''
    print(qresult)
    print()
    
    '''FINDING INFORMATION OF MATCHES'''

    for j in qresult:
        best_match = qresult[1]
        himself = qresult[0]
        if j==himself:
            continue
        elif j == best_match:
            print("This is your best match!")
        name, email = j[0].split("#")
        score = j[1]
        num = 0
        count = -1
        for i in db:
            count += 1
            if i.name == name and i.email == email:
                num = count
                break
        matched = db[num]
        print(f"{matched.name} has score {score} and his/her email is {matched.email}.")
        print(f"{matched.name}'s expectation is {matched.expectation}")
        print()
        

if __name__ == '__main__':
    main()
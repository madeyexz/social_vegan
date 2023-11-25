from person_class import Person
from pinecone_deployment import *

def main():

    pinecone_index = pinecone_init()
    # print(pinecone_index.describe_index_stats())
    
    # a 2d list of id-Person pair, where id = name + email
    # for each entry in the list, create a person object and upsert the vector into pinecone index
    
    '''ADDING USER INFORMATION'''
    usr_data = [["lara",18,False,True,"BJ","A@gmail.com","I am a stone"],["lance",19,True,True,"BJ","B@gmail.com","I am a cat"],["jimmy",25,True,True,"BJ","C@gmail.com","I am a kitten"]]
    
    ppl = []
    for i in usr_data:
        ppl.append(Person(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
    
    with open("data.txt", "w") as f:
        f.write(str(pinecone_fetch(ppl[0], pinecone_index)))
    
    # ppl = [Person(A), Person(B), Person(C)]
    
    # will result in
    # ppl = [
    #     "lara@gmail":Person("lara",18,False,True,"BJ","@gmail.com","I am a capybara"),
    #     "lance@gmail":Person("lance",19,True,True,"BJ","@gmail.com","I am a cat"),
    #     "jimmy@gmail.com":Person("jimmy",25,True,True,"BJ","@gmail.com","I am a dude"),
    # ]
    
    for i in ppl:
        pinecone_vector_upsert(i, pinecone_index)
    
    print(pinecone_index.describe_index_stats())
    
    '''QUERYING'''
    qperson = ppl[-1]
    qresult = pinecone_query(pinecone_index, qperson, 1)
    
    '''PRINTING RESULTS'''
    print(qresult)
    print()
    
    '''FINDING INFORMATION OF MATCHES'''
    
    

    for j in qresult:
        if j == qresult[0]:
            print("This is your best match!")
        name, email = j[0].split("#")
        score = j[1]
        num = 0
        count = -1
        for i in ppl:
            count += 1
            if i.name == name and i.email == email:
                num = count
                break
        matched = ppl[num]
        print(f"{matched.name} has score {score} and his/her email is {matched.email}.")
        print(f"{matched.name}'s expectation is {matched.expectation}")
        print()
        

if __name__ == '__main__':
    main()
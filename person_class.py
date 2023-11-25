from openai import OpenAI
import uuid

wordcount_limit  = 300 # 300 English words

client = OpenAI()

''''NEEDS API COMMUNICATION: CREATING A PERSON'''
'''RECORD EACH PERSON'S CREATION TIME, WE HAVE RATE LIMITS OF 3 REQUEST PER MINUTE AND 200 REQUESTS PER DAY'''

class Person:
    def __init__(self, name: str, age: int, man: bool, hetero: bool, city: str, email: str, expectation: str):
        self.name = name
        self.id = name + "#" + email # generate a unique id for each person
        self.age = age
        self.man = man # if user is a man
        self.hetero = hetero # if user is heterosexual
        self.city = city
        self.email = email
        self.expectation = expectation # expectation from the person
        self.wordcount = self.expectation.count(' ') + 1
        self.match_result_id = [] # empty by default
        self.token_cost = 0 # 0 by default
        self.vector = [] # empty by default
        
        # generating the vector for expectation
        if self.wordcount <= wordcount_limit:
            response = client.embeddings.create(
                input = self.expectation,
                model = "text-embedding-ada-002"
            )
            self.token_cost = response.usage.total_tokens
            self.vector = response.data[0].embedding # a list with 1536 elements
        else:
            ''''NEEDS API COMMUNICATION'''
            print("Word count limit exceeded, please try again")
        
        ''''NEEDS API COMMUNICATION'''
        print(f"{self.id} created successfully")
        
    def __str__(self):
        return f"{self.name} has ID {self.id}."

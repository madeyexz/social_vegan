from person_class import Person
from pinecone_module import *
# from json_local_db import *
import json
from chatbot_module import *

def main():

    preset_data = [
        ["James", 34, True, True, "US", "james34@example.com",
        "In an intimate relationship, I value honesty and communication above all. Trust is the foundation of any strong relationship, and it's something I take very seriously. I believe in being open and transparent with my partner, sharing thoughts, feelings, and experiences freely. Mutual respect is also paramount; respecting each other's individuality, space, and opinions helps in nurturing a healthy bond. I also think it's important to support each other's goals and dreams, as growing together strengthens the relationship. Lastly, a sense of humor and the ability to enjoy life's simple moments together make every day special."],
        ["Sophia", 28, False, True, "UK", "sophia28@example.co.uk",
        "For me, an intimate relationship is built on mutual respect and understanding. I value a partner who listens and communicates effectively. It's important to feel emotionally safe and supported. I believe in equality in a relationship, where both partners contribute equally to decision-making and problem-solving. Sharing common interests and values is key, but I also appreciate the importance of having individual hobbies and time apart. Kindness, patience, and a willingness to grow together are qualities I hold dear."],
        ["Luis", 30, True, False, "MX", "luis30@example.mx",
        "In a relationship, I prioritize loyalty and commitment. I believe in standing by each other through thick and thin, and in the importance of being faithful. Emotional connection is crucial, and I value deep, meaningful conversations that strengthen our bond. I also think it's important to maintain a sense of independence within a relationship, allowing each other space to grow. Shared values and a similar outlook on life are important to me, as they foster a deeper understanding and connection."],
        ["Aisha", 25, False, True, "AE", "aisha25@example.ae",
        "I believe the core of any intimate relationship is mutual respect and empathy. Understanding and caring for each other's emotional and physical well-being is paramount. I value honesty and integrity; being truthful and upfront builds trust. I also look for a sense of humor and light-heartedness in a partner, as I believe laughter and joy are essential in life. Supporting each other's ambitions and being each other's cheerleader in life's journey is something I hold in high regard."],
        ["Raj", 29, True, True, "IN", "raj29@example.in",
        "Trust and mutual respect are the cornerstones of any relationship for me. I believe in maintaining an honest and transparent communication channel with my partner. It's important to respect each other's boundaries and personal space. I value a partner who is understanding and patient, as these qualities help in navigating through tough times together. Sharing common interests and passions adds joy to the relationship, but I also appreciate and encourage having individual pursuits."],
        # ["Emma", 32, False, False, "CA", "emma32@example.ca",
        # "In my view, a strong intimate relationship is based on trust, communication, and mutual support. I value a partner who is open-minded and respects my opinions and decisions. Emotional intelligence and the ability to empathize with each other are crucial. I look for a deep emotional connection rather than just a physical one. It's important for me to share life goals and values with my partner, as this creates a strong foundation for a lasting relationship."],
        # ["Ken", 27, True, True, "JP", "ken27@example.jp",
        # "Honesty and loyalty are the most important values to me in a relationship. I believe in being faithful and dedicated to my partner. A strong emotional connection and the ability to communicate effectively are key. I value a relationship where both individuals can grow and learn from each other. Sharing similar interests and life goals is important, but I also respect and appreciate our differences. A sense of humor and the ability to enjoy the simple things in life together are essential."],
        # ["Nadia", 31, False, True, "ZA", "nadia31@example.za",
        # "I value trust, respect, and understanding in a relationship. Being able to communicate openly and honestly is crucial for me. I believe in supporting each other's dreams and aspirations, while also being there through challenges. A balance of independence and togetherness is important; it's essential to maintain our individual identities while building a life together. Kindness, empathy, and a good sense of humor are qualities I look for in a partner."],
        # ["Marco", 35, True, True, "IT", "marco35@example.it",
        # "In a relationship, I prioritize respect, honesty, and loyalty. I believe in being completely transparent with my partner and expect the same in return. Emotional support is crucial, and I value a partner who is empathetic and understanding. Sharing common interests and values is important, but I also appreciate and respect our differences. A sense of adventure and the willingness to try new things together keeps the relationship exciting and growing."],
        # ["Leila", 26, False, True, "FR", "leila26@example.fr",
        # "Core values for me in a relationship include mutual respect, trust, and open communication. I believe it's important to be supportive of each other's goals and to encourage personal growth. Understanding and patience are key in navigating through the ups and downs of a relationship. I value a partner who is not only a lover but also a friend. Sharing common interests is great, but I also appreciate the beauty of our differences. A relationship should be a safe space for both individuals to be their true selves."]
    ]
    # initialize the database
    # db_reset('user.db')
    # format the data
    
    # initialize the fucking database
    # a = preset_data[0]
    # db_data_insert(Person(a[0],a[1],a[2],a[3],a[4],a[5],a[6]).to_dict(),'user.db')
    
    for i in preset_data:
        if i[0] + '#' + i[5] in db_get_all_ids('user.db'):
            continue
        else:
            db_data_insert(Person(i[0],i[1],i[2],i[3],i[4],i[5],i[6]).to_dict(),'user.db')
    
    # get all ids
    ids = db_get_all_ids('user.db')
    
    # initialize the pinecone index
    index = pinecone_init('socialvegan')
    
    # insert the vectors into pinecone index
    for i in ids:
        pinecone_vector_upsert(i, index)
        print(f"Inserted {i} into pinecone successfully")
    
    # for every entry, query its k nearest neighbors
    for i in ids:
        pinecone_query(index, i, 3)
        print(f"Queried {i} in pinecone successfully")
    
    # print the results without vector col
    db_print_without_vector('user.db')
    
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
            matched_name, matched_exp, matched_email = db_data_read(matched_id, 'name', database_path), db_data_read(matched_id, 'expectation', database_path), db_data_read(matched_id, 'email', database_path)
            prompt = f"My expectation is '{user_exp}', and his/her expectation is '{matched_exp}'. Why are we a good match?"
            result = chatbot_completion(prompt)
        
        print(f"You ({user_name}) are matched with {matched_name} with a score of {matched_score}!")
        print(f"Your expectation is: {user_exp}")
        print(f"{matched_name}'s expectation is: {matched_exp}, and his/her email is {matched_email}")
        print(result)
        print()
        print()
        

if __name__ == '__main__':
    # test()
    main()
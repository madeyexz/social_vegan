import sqlite3
import json
from typing import Any
from person_class import Person

def db_data_insert(data: dict, database: str) -> None:
    '''create a SQLite database and insert one set of data into it, if the data encounters UNIQUE constraint, replace it altogether'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # Create table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            man BOOLEAN,
            hetero BOOLEAN,
            city TEXT,
            email TEXT,
            expectation TEXT,
            wordcount INTEGER,
            match_result_id TEXT,
            token_cost INTEGER,
            vector TEXT
        )
        ''')

        # Insert data into table
        try:
            cursor.execute('''
        INSERT INTO persons (id, name, age, man, hetero, city, email, expectation, wordcount, match_result_id, token_cost, vector)
        VALUES (:id, :name, :age, :man, :hetero, :city, :email, :expectation, :wordcount, :match_result_id, :token_cost, :vector)
        ''', data)
        
        except sqlite3.IntegrityError:
            cursor.execute('''
            INSERT OR REPLACE INTO persons (id, name, age, man, hetero, city, email, expectation, wordcount, match_result_id, token_cost, vector)
            VALUES (:id, :name, :age, :man, :hetero, :city, :email, :expectation, :wordcount, :match_result_id, :token_cost, :vector)
            ''', (data))

def db_data_read(id: str, info: str, database: str) -> Any:
    '''Extract certain info of a certain id from the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # Validate info to prevent SQL injection
        if info not in ['name', 'age', 'man', 'hetero', 'city', 'email', 'expectation', 'wordcount', 'match_result_id', 'token_cost', 'vector']:
            raise ValueError("Invalid info parameter")

        cursor.execute(f"SELECT {info} FROM persons WHERE id = ?", (id,))
        result = cursor.fetchone()

    return result[0] if result else None

def db_data_update(id: str, info: str, new_value: Any, database: str) -> None:
    '''Update certain info of a certain id in the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # Validate info to prevent SQL injection
        if info not in ['name', 'age', 'man', 'hetero', 'city', 'email', 'expectation', 'wordcount', 'match_result_id', 'token_cost', 'vector']:
            raise ValueError("Invalid info parameter")

        cursor.execute(f"UPDATE persons SET {info} = ? WHERE id = ?", (new_value, id))

def db_matched_id_update(id: str, new_value_pair: list, database: str) -> None:
    '''Update only the matched_id part for certain id in the SQLite database'''
    # grab the original match_result_id and then add the list to it direct, list1+list2
    matched_lst = json.loads(db_data_read(id, 'match_result_id', database))
    print(matched_lst)
    matched_lst.append(new_value_pair)
    print(matched_lst)
    new_lst = json.dumps(matched_lst)
    
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute(f"UPDATE persons SET match_result_id = ? WHERE id = ?", (new_lst, id))


def db_print_all(database: str) -> None:
    '''Print all data in the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM persons")
        result = cursor.fetchall()

    for row in result:
        print(row)
    return None


def db_print_without_vector(database: str) -> None:
    '''Print all data in the SQLite database without the vector column'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # Assuming you know the column names and 'vector' is one of them
        # Modify the column list as per your table schema
        cursor.execute("SELECT id, name, age, man, hetero, city, email, expectation, wordcount, match_result_id, token_cost FROM persons")
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(row) 
        
def print_entire_database(db_path):
    # Connect to the SQLite database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Retrieve a list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Iterate over all tables
        for table_name in tables:
            print(f"Table: {table_name[0]}")
            print("-" * 40)

            # Retrieve all data from each table
            cursor.execute(f"SELECT * FROM {table_name[0]}")
            rows = cursor.fetchall()

            # Get column names
            column_names = [description[0] for description in cursor.description]

            # Print column names
            print(", ".join(column_names))

            # Print rows
            for row in rows:
                print(row)
                
            print("\n" + "=" * 40 + "\n")
    return None

def db_count_rows(database: str) -> int:
    '''Count the number of rows in the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM persons")
        result = cursor.fetchone()

    return result[0] if result else None

def db_print_all_ids(database: str) -> None:
    '''Print all ids in the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM persons")
        result = cursor.fetchall()

    for row in result:
        print(row[0])
    return None

def db_get_all_ids(database: str) -> list:
    '''Get all ids in the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM persons")
        result = cursor.fetchall()

    return [row[0] for row in result] if result else None

def db_delete_id(id: str, database: str) -> None:
    '''Delete a certain id from the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM persons WHERE id = ?", (id,))
    return None

def db_reset(database: str) -> None:
    '''Reset the SQLite database'''
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
 
        cursor.execute("DROP TABLE IF EXISTS persons")
    return None

# testing
def main():
    # Example usage
    database_path = 'user.db'
    person_id = 'john#A@gmail'
    info_to_read = 'age'
    info_to_update = 'city'
    new_city = 'New York'

    # Insert data
    person_data = {
        'name' : 'john',
        'id' : 'john#A@gmail',
        'age' : 18,
        'man' : False,
        'hetero' : True,
        'city' : 'BJ',
        'email' : 'A@gmail',
        'expectation' : 'I am a stone',
        'wordcount' : 4,
        'match_result_id' : json.dumps([]),
        'token_cost' : 0,
        'vector' : json.dumps([1.2,2.3,3.4,4.5])
    }
    
    preset_data = [["lara",18,False,True,"BJ","A@gmail.com","I am a stone"],["lance",19,True,True,"BJ","B@gmail.com","I am a cat"],["jimmy",25,True,True,"BJ","C@gmail.com","I am a kitten"]]
    
    # print(db_count_rows(database_path))
    db_print_all_ids(database_path)
    # a function that changes preset_data into the foramt of person_data
    # for i in preset_data:
    #     db_data_insert(Person(i[0],i[1],i[2],i[3],i[4],i[5],i[6]).to_dict(),database_path)
    
    # # db_print_all(database_path)
    # db_data_insert(person_data, database_path)
    # db_print_all(database_path)

    # # Read data
    # age = db_data_read(person_id, info_to_read, database_path)
    # # print(f"Age of {person_id}: {age}")

    # # Update data
    # db_data_update(person_id, info_to_update, new_city, database_path)
    # # print(f"Updated city of {person_id} to {new_city}")
    # db_print_all(database_path)

if __name__ == '__main__':
    main()
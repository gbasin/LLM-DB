import json
import sys

from gptcache import cache
from gptcache.adapter import openai
from gptcache.processor.pre import all_content

from src import openai_api

class LLM:
    def classify_command(self, command):
        system_prompt = "You are a database language model. Given the following command, classify it into a list of actions (INSERT or QUERY) and their associated command text. Respond only with valid JSON."
        examples = [
            {"name": "example_user", "content": "Insert a new book with title '1984' by George Orwell."},
            {"name": "example_assistant", "content": '[{"action": "INSERT", "command": "Insert a new book with title \'1984\' by George Orwell."}]'},
            {"name": "example_user", "content": "Find all books published before 2000."},
            {"name": "example_assistant", "content": '[{"action": "QUERY", "command": "Find all books published before 2000."}]'},
            {"name": "example_user", "content": "Add an animal, a cat named Whiskers, aged 2 and search for all animals younger than 5."},
            {"name": "example_assistant", "content": '[{"action": "INSERT", "command": "Add an animal, a cat named Whiskers, aged 2"}, {"action": "QUERY", "command": "Search for all animals younger than 5."}]'},
        ]

        prompt = command
        try:
            classified_command = chat_completion(system_prompt, examples, prompt)
            return json.loads(classified_command)
        except Exception as e:
            print(f"Error while classifying command: {e}")
            return []

    def process_insert(self, command):
        system_prompt = "You are a database language model. Given the following INSERT command, transform it into JSON format. Respond only with valid JSON."
        examples = [
            {"name": "example_user", "content": "Insert a new book with title '1984' by George Orwell."},
            {"name": "example_assistant", "content": '{"type": "book", "title": "1984", "author": "George Orwell"}'},
            {"name": "example_user", "content": "Add a painting titled 'Starry Night' by Van Gogh."},
            {"name": "example_assistant", "content": '{"type": "painting", "title": "Starry Night", "artist": "Van Gogh"}'},
            {"name": "example_user", "content": "Add an animal, a cat named Whiskers, aged 2."},
            {"name": "example_assistant", "content": '{"type": "animal", "species": "cat", "name": "Whiskers", "age": 2}'},
        ]

        prompt = command
        try:
            processed_command = chat_completion(system_prompt, examples, prompt)
            return json.loads(processed_command)
        except Exception as e:
            print(f"Error while processing insert command: {e}")
            return {}

    def process_query(self, json_entry, query):
        system_prompt = "You are a database language model. Given the following database entry and query, determine whether the entry meets the query criteria. Respond only with Yes or No."
        examples = [
            {"name": "example_user", "content": '{"database_entry": {"type": "book", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "publication_year": 1951}, "query": "Find all books published before 2000."}'},
            {"name": "example_assistant", "content": 'Yes'},
            {"name": "example_user", "content": '{"database_entry": {"type": "movie", "title": "Inception", "director": "Christopher Nolan", "release_year": 2010}, "query": "Find all movies released in 2010."}'},
            {"name": "example_assistant", "content": 'Yes'},
            {"name": "example_user", "content": '{"database_entry": {"type": "product", "name": "iPhone 12", "price": 799}, "query": "Find all products with a price below $500."}'},
            {"name": "example_assistant", "content": 'No'}
        ]

        prompt = f"Database Entry: {json_entry}, Query: {query}"
        try:
            processed_query = chat_completion(system_prompt, examples, prompt)
            return processed_query.lower() == 'yes'
        except Exception as e:
            print(f"Error while processing query: {e}")
            return False

class DatabaseManager:
    def __init__(self, filename):
        self.filename = filename

    def insert_data(self, data):
        try:
            with open(self.filename, 'a') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            print(f"Error while inserting data: {e}")

    def retrieve_data(self):
        try:
            with open(self.filename, 'r') as f:
                return [json.loads(line) for line in f.readlines()]
        except Exception as e:
            print(f"Error while retrieving data: {e}")
            return []

class CommandProcessor:
    def __init__(self, llm, db_manager):
        self.llm = llm
        self.db_manager = db_manager

    def handle_command(self, command):
        try:
            classified_commands = self.llm.classify_command(command)
            results = []
            for classified_command in classified_commands:
                if classified_command['action'] == 'INSERT':
                    data = self.llm.process_insert(classified_command['command'])
                    self.db_manager.insert_data(data)
                    results.append(data)
                elif classified_command['action'] == 'QUERY':
                    data = self.db_manager.retrieve_data()
                    query_results = []
                    for entry in data:
                        if self.llm.process_query(json.dumps(entry), classified_command['command']):
                            query_results.append(entry)
                    results.append(query_results)
            return results
        except Exception as e:
            print(f"Error while handling command: {e}")
            return []

def chat_completion(system_message, examples, prompt):
    # This function will call the LLM API with the given prompt and return the response
    response = openai_api.generate_chat_completion(prompt, system_message, examples);
    return response['choices'][0]['message']['content'];

def main():
    # use gptcache
    cache.init(pre_embedding_func=all_content) # use all prompts and full history as cache key
    cache.set_openai_key()
    
    # init objects
    llm = LLM()
    db_manager = DatabaseManager("../data/database.txt")
    command_processor = CommandProcessor(llm, db_manager)

    # process command
    try:
        results = command_processor.handle_command(' '.join(sys.argv[1:]))
        print(results)
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()
    
    # To insert data
    # python filename.py "Insert John Doe with age 25."

    # To query data
    # python filename.py "Find all people older than 20."
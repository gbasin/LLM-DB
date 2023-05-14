import json
import sys

class LLM:
    def process_command(self, command):
        # Construct a prompt to instruct the LLM to extract data from the command into JSON format
        prompt = f"Transform the following command into JSON format: '{command}'"
        processed_command = chat_completion(prompt)
        return json.loads(processed_command)

    def process_query(self, json_entry, query):
        # Construct a prompt to instruct the LLM to compare the JSON entry with the query criteria
        prompt = f"Does the following database entry '{json_entry}' meet the criteria specified in this query: '{query}'?"
        processed_query = chat_completion(prompt)
        return processed_query.lower() == 'yes'

class DatabaseManager:
    def __init__(self, filename):
        self.filename = filename

    def insert_data(self, data):
        with open(self.filename, 'a') as f:
            f.write(json.dumps(data) + '\n')

    def retrieve_data(self):
        with open(self.filename, 'r') as f:
            return [json.loads(line) for line in f.readlines()]

class CommandProcessor:
    def __init__(self, llm, db_manager):
        self.llm = llm
        self.db_manager = db_manager

    def handle_command(self, command):
        data = self.llm.process_command(command)
        self.db_manager.insert_data(data)

    def handle_query(self, query):
        data = self.db_manager.retrieve_data()
        results = []
        for entry in data:
            if self.llm.process_query(json.dumps(entry), query):
                results.append(entry)
        return results

def chat_completion(prompt):
    # This function will call the LLM API with the given prompt and return the response
    pass

def main():
    llm = LLM()
    db_manager = DatabaseManager("../data/database.txt")
    command_processor = CommandProcessor(llm, db_manager)

    if sys.argv[1] == 'insert':
        command_processor.handle_command(sys.argv[2])
    elif sys.argv[1] == 'query':
        results = command_processor.handle_query(sys.argv[2])
        print(results)

if __name__ == "__main__":
    main()
    
    # To insert data
    # python filename.py insert "Insert John Doe with age 25."

    # To query data
    # python filename.py query "Find all people older than 20."
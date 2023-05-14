import json
import sys

from src import openai_api

class LLM:
    def classify_command(self, command):
        # Construct a prompt to instruct the LLM to classify the command
        prompt = f"""
Given the following command, classify it into a list of actions (INSERT or QUERY) and their associated command text:

Example 1:
Input: "Insert John Doe with age 25."
Output: [{"action": "INSERT", "command": "Insert John Doe with age 25."}]

Example 2:
Input: "Find all people older than 20."
Output: [{"action": "QUERY", "command": "Find all people older than 20."}]

Input: "{command}"
"""
        classified_command = chat_completion(prompt)
        return json.loads(classified_command)

    def process_insert(self, command):
        # Construct a prompt to instruct the LLM to extract data from the insert command into JSON format
        prompt = f"""
Given the following INSERT command, transform it into JSON format:

Example:
Input: "Insert John Doe with age 25."
Output: {"name": "John Doe", "age": 25}

Input: "{command}"
"""
        processed_command = chat_completion(prompt)
        return json.loads(processed_command)

    def process_query(self, json_entry, query):
        # Construct a prompt to instruct the LLM to compare the JSON entry with the query criteria
        prompt = f"""
Given the following database entry and query, determine whether the entry meets the query criteria:

Example:
Database Entry: {"name": "John Doe", "age": 25}
Query: "Find all people older than 20."
Output: Yes

Database Entry: {json_entry}
Query: {query}
"""
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

def chat_completion(prompt):
    # This function will call the LLM API with the given prompt and return the response
    response = openai_api.generate_chat_completion(prompt);
    return response['choices'][0]['message']['content'];

def main():
    llm = LLM()
    db_manager = DatabaseManager("../data/database.txt")
    command_processor = CommandProcessor(llm, db_manager)

    results = command_processor.handle_command(' '.join(sys.argv[1:]))
    print(results)
    

if __name__ == "__main__":
    main()
    
    # To insert data
    # python filename.py "Insert John Doe with age 25."

    # To query data
    # python filename.py "Find all people older than 20."
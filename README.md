# LM-DB: a database powered by language models
### "LM is all you need"
This project introduces a new type of database that uses Language Models (LMs) to perform all operations. The main objective is to allow users to interact with the database using natural language.

For inserting data and querying, we use natural language inputs which are then processed by the LM. The LM interprets the input, and either inserts it into the data store, or queries the data store for matching entries.

The data store is a flat file where each line represents a separate entry in the database.

## Example 1
```
% python src/main.py "create a new capability \
to allow web browsing with the {browse} command, add another capability to send emails with \
 the {email} command"

INSERTED: {'type': 'capability', 'function': 'web_browsing', 'command': 'browse'}
INSERTED: {'type': 'new_capability', 'command': 'email', 'command_arg': '{email}'}

% cat data/database.txt
{"type": "capability", "function": "web_browsing", "command": "browse"}
{"type": "new_capability", "command": "email", "command_arg": "{email}"}

% python src/main.py "retrieve all capabilities that may provide access to wikipedia data"

Entry: {"type": "capability", "function": "web_browsing", "command": "browse"}
Query result: The 'capability' with 'function' 'web_browsing' can potentially provide access to Wikipedia data by browsing the Wikipedia website. Therefore: (90)
Match probability: 90%

Entry: {"type": "new_capability", "command": "email", "command_arg": "{email}"}
Query result: This entry is about a 'new_capability' with a 'command' for 'email', which is not related to providing access to Wikipedia data. Therefore: (0)
Match probability: 0%

Results:
["{'type': 'capability', 'function': 'web_browsing', 'command': 'browse'}"]
```

# Motivation
todo


# Setup

1. Create a `.env` file with your openai api key (see `.env.example`)
2. Install Pipenv if you don't have it already. You can install it using pip:

   ```bash
   pip install pipenv
   ```
3. Clone the repository or download the project files to your local machine.
4. Navigate to the project directory using the terminal or command line.
5. Create a new virtual environment and install project dependencies with Pipenv:

   ```bash
   pipenv install
   ```

# Running

1. Activate the Pipenv virtual environment:
   ```bash
   pipenv shell
   ```
2. Run the project:
   ```bash
   %python src/main.py "Insert John Doe with age 25 and find all people older than 20."

   INSERTED: {'name': 'John Doe', 'age': 25}

   Entry: {"name": "John Doe", "age": 25}
   Query result: This entry has 'John Doe' with an 'age' of 25, which is older than 20. Therefore: (100)
   Match probability: 100%

   Results:
   ["{'name': 'John Doe', 'age': 25}"]
   ```

# Dev notes

- If you need to install additional dependencies, you can use the `pipenv install` command followed by the package name.

- Make sure to update the `Pipfile` if you add or remove dependencies. You can do this by running `pipenv install package_name`.

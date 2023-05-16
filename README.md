# LM-DB: a database powered by language models
### "LM is all you need"
This project introduces a new type of database that uses Language Models (LMs) to perform all operations. The main objective is to allow users to interact with the database using natural language.

For inserting data and querying, we use natural language inputs which are then processed by the LM. The LM interprets the input, and either inserts it into the data store, or queries the data store for matching entries.

The data store is a flat file where each line represents a separate entry in the database.

## Example
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
    python main.py "Insert John Doe with age 25 and find all people older than 20."
   ```

# Dev notes

- If you need to install additional dependencies, you can use the `pipenv install` command followed by the package name.

- Make sure to update the `Pipfile` if you add or remove dependencies. You can do this by running `pipenv install package_name`.

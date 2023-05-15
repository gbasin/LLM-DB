# LM-DB: a database powered by language models
### "LM is all you need"
This project introduces a new type of database that uses Language Models (LMs) to perform all operations. The main objective is to allow users to interact with the database using natural language, which is then interpreted by an LM and executed on a text-based data store.

For inserting data and querying, we use natural language inputs which are then processed by the LM. The LM interprets the input, and either inserts it into the data store (in JSON), or queries the data store for matching entries (returning the JSON).

The data store used in this project is a flat file where each line represents a separate entry in the database. This was chosen for simplicity and because it is well-suited for the iterative approach we use for queries.

# Motivation
todo

# What it can do
### Unstructured and inference-based queries
LM-DB queries can take advantage of LM-internal knowledge to capture meaning missing from fields or schema

Example: "Find me all authors who wrote dystopian novels." 

If the 'genre' field doesn't exist in the database, an SQL query would fail. The LLM, on the other hand, could infer the genre based on book titles and authors if it has been trained on such data.

Example: "Insert a product named 'iPhone 12' with a price of $799. Then, tell me all the expensive products."

Here, the LLM could infer what 'expensive' means based on the prices of the products in the database, even if 'expensive' hasn't been explicitly defined. This kind of relative and inference-based query would be difficult for a traditional database.


# Setup

1. Make sure you have Python installed. You can download it from the [Python website](https://www.python.org/downloads/).
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

This command will create a new virtual environment and install the necessary dependencies based on the Pipfile.

# Running

1. Activate the Pipenv virtual environment:
   ```bash
   pipenv shell
   ```
2. Run the project:
   ```bash
    python main.py "Insert John Doe with age 25 and find all people older than 20."
   ```
3. When you're done with the project, you can exit the virtual environment:
   ```bash
   exit
   ```

# Dev notes

- If you need to install additional dependencies, you can use the `pipenv install` command followed by the package name.

- Make sure to update the `Pipfile` if you add or remove dependencies. You can do this by running `pipenv install package_name`.
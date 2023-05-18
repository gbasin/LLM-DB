# LMDB: a database powered by language models
## "LM is all you need"
This project is a proof of concept for a new type of database that uses Language Models (LMs) to perform all operations. The main objective is to allow users to interact with the database using natural language. Currently, it supports inserting data and querying it, both with natural language and leveraging whatever reasoning capability is present in the LM.

To process a query, the LM interprets the input, and either inserts it into the data store, or queries the data store for matching entries one at a time. The data store is a flat file where each line represents a separate entry in the database.

To insert data, just describe the entries:
```
% python src/main.py "add a person named john who's 30 years old, and a cat named bob who is 7 yrs old"
INSERTED: {'type': 'person', 'name': 'John', 'age': 30}
INSERTED: {'type': 'animal', 'species': 'cat', 'name': 'Bob', 'age': 7}
```

It's stored in plaintext:
```
% cat data/database.txt
{"type": "person", "name": "John", "age": 30}
{"type": "animal", "species": "cat", "name": "Bob", "age": 7}
```

And finally, query with natural language:
```
% python src/main.py "all living things under 10 years old"

Entry: {"type": "person", "name": "John", "age": 30}
Query result: This entry is of type 'person' and John is a living thing, but his age is 30, which is above the 10-year criterion. Therefore: (0)
Match probability: 0%

Entry: {"type": "animal", "species": "cat", "name": "Bob", "age": 7}
Query result: This entry is about a 'cat' which is a living thing, and its 'age' is 7, which is under 10 years old. Therefore: (100)
Match probability: 100%

Results:
["{'type': 'animal', 'species': 'cat', 'name': 'Bob', 'age': 7}"]
```

## Motivation
LMs, even large ones, will constantly need to be taught new information, or provided data that doesn't exist in their weights. Facts change, people have private data stores, etc. The best way to do this will often be at inference time, by providing the information as context.

Vector embedding search is insufficient. Embedding vectors are not smart enough to perform the kind of reasoning that happens in a forward pass of an LM. Embedding search tends to retrieve lots of irrelevant matches, or even miss content that could be relevant when you apply a little reasoning (like the wikipedia browsing example in the Examples below). You could, of course, use vector search to get lots of candidates, stuff them into a context window (maybe rerank some first?), and ask an LLM about them. The problem is, this doesn't scale -- LLMs get easily confused with more content in the context (check out [Large Language Models Can Be Easily Distracted by Irrelevant Context](https://arxiv.org/pdf/2302.00093.pdf))

If we're building for a world where small LMs are narrowly smart, fast, and run locally (~zero cost), a lot of cool things become possible -- essentially we can build databases that can think. I bet this is likely to be the case within the next few years. As a hint of what's possible already, see [TinyStories](https://arxiv.org/abs/2305.07759) -- 30 million param LMs trained for a narrow task (generating children's stories) exhibiting basic reasoning and getting close to GPT-4 level performance (as assessed by GPT-4).

## Examples
LMDB's are useful when you want your query to use a little bit of reasoning.

For example, you can create a database of some tools that we want the LM to know about, and use the LMDB to look up ones relevant to as a task. Here we add ane mail and web browsing tool, then ask the LMDB to find which tool could be good for getitng data from wikipedia:

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

Using an LM to reason about each potential match for a query gives you much smarter results than vector embedding similarity. Let's compare.

Notice how the vector embeddings are all pretty similar (the first line is the string that we will compare distances to):

```
% python src/scripts/calc_cosine_sim.py "\
  info on what a home appraisal is|\
  home appraisals are necessary for getting a mortgage|\
  tax assessments estimate the value for tax purposes|\
  Tax assessments are not the same as home appraisals|\
  home appraisals estimate the home's value and are a requirement"
1.0000000000000002
0.8862083445084581
0.82672579893429
0.8496773423391857
0.8939081265657459
```

Using techniques like [Hypothetical Document Embeddings (HyDE)](https://arxiv.org/abs/2212.10496) can help but it fails in many cases, like this one:

```
% python src/scripts/calc_cosine_sim.py "\
  a home appraisal is a random number generated by an appraiser|\
  home appraisals are necessary for getting a mortgage|\
  tax assessments estimate the value for tax purposes|\
  Tax assessments are not the same as home appraisals|\
  home appraisals estimate the home's value and are a requirement"
1.0000000000000002
0.8628389021604684
0.82073464427003
0.8495163850290542
0.8783869751576889
```

Of course, the LMDB does a pretty good job. First, insert the facts:

```
% python src/main.py "add a home appraisal fact: they are necessary for getting a mortgage, \
add a tax assessment fact: they estimate the value for tax purposes, \
add another tax assessment fact: they are not the same as a home appraisal, \
add a mortgage fact: home appraisals estimate the home's value and are a requirement"


INSERTED: {'type': 'home_appraisal_fact', 'fact': 'necessary for getting a mortgage'}
INSERTED: {'type': 'fact', 'subject': 'tax assessment', 'description': 'they estimate the value for tax purposes'}
INSERTED: {'type': 'fact', 'topic': 'tax assessment', 'description': 'not the same as a home appraisal'}
INSERTED: {'type': 'mortgage_fact', 'description': "home appraisals estimate the home's value and are a requirement"}
```

Then query. LMDB also has the benefit of providing reasoning for which rows match the query, and some estimate of probability.

```
% python src/main.py "get info that explains what a home appraisal is"

Entry: {"type": "home_appraisal_fact", "fact": "necessary for getting a mortgage"}
Query result: The 'home_appraisal_fact' states it is 'necessary for getting a mortgage', but does not define what a home appraisal is. Therefore: (20)
Match probability: 20%

Entry: {"type": "fact", "subject": "tax assessment", "description": "they estimate the value for tax purposes"}
Query result: The entry is about 'tax assessment' and not directly about 'home appraisal', though they can be connected. The information is somewhat related but doesn't thoroughly explain what a home appraisal is. Therefore: (30)
Match probability: 30%

Entry: {"type": "fact", "topic": "tax assessment", "description": "not the same as a home appraisal"}
Query result: The 'description' in this entry refers to 'tax assessment' being different from a 'home appraisal', but doesn't directly explain what a home appraisal is. Therefore: (5)
Match probability: 5%

Entry: {"type": "mortgage_fact", "description": "home appraisals estimate the home's value and are a requirement"}
Query result: The 'mortgage_fact' 'description' states that 'home appraisals estimate the home's value', which explains what a home appraisal is. Therefore: (100)
Match probability: 100%

Results:
['{\'type\': \'mortgage_fact\', \'description\': "home appraisals estimate the home\'s value and are a requirement"}']
```


## Setup

1. Create a `.env` file with your openai api key (see `.env.example`)
2. Install Pipenv if you don't have it already. You can install it using pip:

   ```bash
   pip install pipenv
   ```
3. Create a new virtual environment and install project dependencies with Pipenv:

   ```bash
   pipenv install
   ```
4. Activate the Pipenv virtual environment:
   ```bash
   pipenv shell
   ```
5. Run the project:
   ```bash
   % python src/main.py "Insert John Doe with age 25 and find all people older than 20."

   INSERTED: {'name': 'John Doe', 'age': 25}

   Entry: {"name": "John Doe", "age": 25}
   Query result: This entry has 'John Doe' with an 'age' of 25, which is older than 20. Therefore: (100)
   Match probability: 100%

   Results:
   ["{'name': 'John Doe', 'age': 25}"]
   ```

## Dev notes
- The database is stored in `data/database.txt`
- The project uses `gptcache` which caches responses from LM queries, reusing them when possible (makes testing much faster!). These are currently stored in a `data_map.txt` file.

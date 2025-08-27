# flybot

Flybot is a customer support bot for an airline company. It helps users research and make travel arrangements.

This code is inspired by Langgraph tutorial that can be accessed [here](https://langchain-ai.github.io/langgraph/tutorials/customer-support/customer-support/) and it extends to a Python package that can be deployed by any airline company that wants to have a chatbot for personalized customer service.

## Getting started

### Download databases

I am using [Swiss Airline](https://storage.googleapis.com/benchmarks-artifacts/travel-db/travel2.sqlite) data from Google API. To download it, you can use the function `flybot.dataprep.get_data` to save a copy on your local machine.

```python
from flybot.dataprep import get_data

# Define your path to save data.
local_file = './travel2.sqlite'
backup_file = './travel2.backup.sqlite'

get_data(file=local_file, backup_file=backup_file)
```

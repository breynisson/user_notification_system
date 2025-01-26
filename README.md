# User Notification System

![Python CI](https://github.com/breynisson/user_notification_system/actions/workflows/python-ci.yml/badge.svg)

[Allure Test Report](https://breynisson.github.io/user_notification_system/)

## Description
The User Notification System is a simple system that allows clients to send messages to the server and fetch the 
status of the clients. The system is implemented using gRPC and Python.

The client can send a simple "Hello" or "Goodbye" message to the server. The server will then store the message and
the status of the client is updated.  If a client has sent a "Hello" message, the status will be "Online". 
If the client has sent a "Goodbye" message, the status will be "Offline". 
The client can then fetch the status of the client or all clients.


## Usage
This project uses Poetry for dependency management. Please follow the instruction on how to install Poetry 
[here](https://python-poetry.org/docs/#installation). We also use poetry scripts to run the commands.

In order to use the project, you need to follow the steps below:
- Clone the repository
- Install the dependencies: `poetry install`
- Generate the protobuf files: `poetry run generate-grpc`
- Activate the Poetry virtual environment: `eval $(poetry env activate)`
- Start the server: `poetry run start-server`
- Send messages to the server: `poetry run send-message {{client_id}} {{message}}`,  
where {{client_id}} is the id of the client and {{message}} is the message you want to send.
- Fetch client status: `poetry run fetch-status {{client_id}}`
- Fetch all clients status: `poetry run fetch-all-statuses`

## Testing
To run the tests, you can use the following command: `poetry run pytest`.
If you want to generate reports from the tests, you can use the following command: 
`poetry run pytest-allure`, followed by `poetry run generate-allure-report`.
Note, this assumes that you have Allure installed on your machine. If you don't have Allure installed, 
you can follow the instructions [here](https://allurereport.org/docs/install/).

We have also set up a GitHub Action that runs the tests and generates the Allure report. You can find the report
[here](https://breynisson.github.io/user_notification_system/).

## Further Improvements
It would be good to containerize the application. A Dockerfile for the Server and Client would be created. 
And a docker-compose file to run the application. This would make it easy to run the application.

## Notes:
There was a problem with the namedlist.py file in the virtual environment used during development. 
The problem was that the collections.Mapping attribute has been deprecated and removed in Python 3.10. 
This was solved by patching the namedlist.py file with `collections.abc.Mapping`:  
- Locate the namedlist.py file in your virtual environment.  
- Open the file and replace `_collections.Mapping` with `_collections.abc.Mapping`.  

While this fix worked, it is not
recommended to modify the files in the virtual environment. 
Interestingly, the problem was not present when running the tests in the GitHub Action. 
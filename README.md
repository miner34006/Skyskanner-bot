# Ticket parser for vk

This program allows you to search for flights according to various criteria with notification when their cost decreases.
The program is built on microservice architecture. It is divided into 3 services (in plans to make 4 services with a database): 
* controller, 
* bot, 
* scanning system (parser).

The controller receives messages from users via vk longPoll server and sends instructions for the bot. Depending on the type of instruction, the bot determines the necessary actions and sends a response to the user.

## Getting Started

For using this bot, just change the GROUP_TOKEN variable in api.py file on your vk group token.

### Installing

To install the system run the command 
```docker-compose up```. 
Bot started its work. Send to it any message and follow the directions.

## Running the tests

All tests located in /tests folder. Run tests using:

```
python tests/yourTest.py
```

## Authors

* **Polianok Bogdan**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


# StuyBook by Team snip_snip
## Roster and Role:
- Tammy Chen (Flask App Creator)
- Grace Mao (HTML/Jinja/JavaScript)
- Derek Leung (Database & Project Manager)

## Project Description
Our project is aimed towards providing a fully functional networking site for Stuyvesant students, mostly geared towards self-management, entertainment, and community. By incorporating REST APIs, JavaScript, Flask, and databases managed by SQLite, our site will allow users to meet other Stuy students and develop their personal profiles for multiple uses.

## APIs Utilized:
[PurgoMalum](https://www.purgomalum.com/)
  - This API allows curse words to be censored with an asterisk. We use this API to assure that no curse words are used in posts.

[Anagrams](http://www.anagramica.com/api)
  - We use this API to make our anagrams game, it will give all the word combinations of a given set of random words. 

[The Open Trivia API](https://opentdb.com/api_config.php)
  - We use this API to get trivia questions for our trivia game. It will provide a collection of trivia questions. 

## How to Run the Project:
- We are assuming that the user has installed Python3 and pip in their environment
- If not, install Python3 from https://www.python.org/downloads/
- pip comes installed with Python by default

#### To clone the project:
``` bash
$ git clone git@github.com:KingDerek1/DerekIsCool.git	
``` 

#### To create a virtual environment and install all packages in the virtual environment:	
```bash	
$ python3 -m venv <name of virtual environment>	
$ . ~/<name of virtual environment>/bin/activate  	
(venv)$ cd <name of cloned directory>	
(venv)/<name of cloned directory>$ pip3 install -r doc/requirements.txt	
```
#### To run the project:
**Note: No API keys are needed for this project to run, so this should run without any issues.**
``` bash
$ cd <name of cloned directory>	
/<name of cloned directory>$ python3 app.py	
```

View the webpage by opening a web browser and visiting: http://127.0.0.1:5000/	

-----------
© Copyright 2020 Team snip_snip -- Tammy Chen, Grace Mao & Derek Leung

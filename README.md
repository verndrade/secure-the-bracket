﻿# secure-the-bracket
Hack for Good Project as part of Summer Hackathon

### Set up instructions for local development:
0. Set up python virtual environment.  
    - `python3 -m venv hack-env`
    - `source hack-env/bin/activate`

1. `git clone https://github.com/verndrade/secure-the-bracket`  
2. In `hackathon/settings.py`, comment out the mysql databases block and uncomment the sqllite block.
3. If mysql is not already installed, download with `brew install mysql`
4. From the root folder, run `pip install -r requirements.txt`  
    - If using mac, make sure you have pip3 installed and then type the above statement with pip3 :)

For initial setup and for any changes to the models data, run:
- `python manage.py makemigrations`
- `python manage.py migrate`  
- `python manage.py runserver`  

To load test data, run
- `python manage.py loaddata bracket`

﻿# secure-the-bracket

### Set up instructions:
git clone https://github.com/verndrade/secure-the-bracket
comment out the databases mysql block and uncomment the sqllite block
go to the folder with manage.py
run "pip install -r requirements.txt"
python manage.py makemigrations 
python manage.py migrate 
python manage.py runserver

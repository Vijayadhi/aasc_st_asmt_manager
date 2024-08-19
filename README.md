## This is project build using django framework of python.

# To run and execute the project,

1. downlaod and extract the files

2. open the folder in the command prompt

3. create the virtual environment using `python -m  venv venv`

4. after creating the virtual environment activate it
`.venv\Scripts\activate`

5. then to install the packages,

`pip install -r requirements.txt`
6. once the installation is completed just run the project using

`python manage.py runserver`

7. If need to backup the data from the database into json, 
    1. Dumping all the data `python manage.py loaddata datas.json`
   2. Dumping based on the tables `python manage.py dumpdata auth.Group --indent 2 > groups.json`
    3. Dumping tables with its relations table, `python manage.py dumpdata auth.Group auth.Permission --indent 2 > groups_with_permissions.json`
   
8. load the groups with its permissions if the db was flused or deleted
`python manage.py loaddata groups.json`

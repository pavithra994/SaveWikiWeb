# open the SaveWikiWeb folder in windows powershell
# activate the virtual envirment:
    .\env\Scripts\activate

# run makemigrarations and migrate commonds
    python manage.py makemigrations
    python manage.py migrate

# run the django server
    python manage.py runserver

# you can access the web app via http://127.0.0.1:8000/




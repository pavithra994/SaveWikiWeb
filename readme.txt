Building a Wikipedia file Upload Service to Google Drive using OAuth 2.0

From this website, you can upload any Wikipedia file to Google drive by given the URL with this very minimalistic application.
This system provides OAuth2 social authentication support for applications in Django Framework.
The aim of this package is to help set up social authentication for the application. It also helps setting up OAuth2 provider.
This package relies on python-social-auth and django-oauth-toolkit.

# open the SaveWikiWeb folder in windows powershell
# activate the virtual envirment:
    .\env\Scripts\activate

# run makemigrarations and migrate commonds
    python manage.py makemigrations
    python manage.py migrate

# run the django server
    python manage.py runserver

# you can access the web app via http://127.0.0.1:8000/




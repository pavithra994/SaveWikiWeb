import os

import httplib2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.conf import settings

from app_user.forms import Upload
from app_user.models import CredentialsModel
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render
from httplib2 import Http



FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/drive',
    redirect_uri='http://127.0.0.1:8000/index',
    prompt='consent')


def gmail_authenticate(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()

    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('drive', 'v3', http=http)
        print('access_token = ', credential.access_token)
        status = True

        return render(request, 'index.html', {'status': status})


def auth_return(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    print("access_token: %s" % credential.access_token)
    return HttpResponseRedirect("/")


def home(request):
    status = True

    if not request.user.is_authenticated:
        return HttpResponseRedirect('admin')

    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()

    try:
        access_token = credential.access_token
        resp, cont = Http().request("https://www.googleapis.com/auth/gmail.readonly",
                                    headers={'Host': 'www.googleapis.com',
                                            'Authorization': access_token})
        print("dfdf",resp,cont)
    except:
        status = False
        print('Not Found')

    if request.method == "POST":
        form = Upload(request.POST,request.FILES)
        if form.is_valid():
            print(form.cleaned_data.get("file").name)
            print(ContentFile(form.cleaned_data.get("file").read()))
            path = default_storage.save(form.cleaned_data.get("file").name, ContentFile(form.cleaned_data.get("file").read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            service = build('drive', 'v3', credentials=credential)
            # media = MediaFileUpload(path, mimetype='application/pdf')
            media = MediaFileUpload(tmp_file, mimetype='image/jpeg')
            file = service.files().create(body={"name":form.cleaned_data.get("file").name},
                                                media_body=media,
                                                fields='id').execute()

            print(file.get('id'))

    else:
        form = Upload()

    return render(request, 'index.html', {'status': status, "form":form})
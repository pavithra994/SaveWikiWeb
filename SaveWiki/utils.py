import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

DOWNLOAD_PREFIX = "https://en.wikipedia.org/api/rest_v1/page/pdf/"

TEMP_FILE = "files/"

class WikipediaController:
    def __init__(self,url:str):
        if url.startswith("https://en.wikipedia.org/wiki/"):
            self.url = url
            self.keyword = url.replace("https://en.wikipedia.org/wiki/","")
        else:
            raise ValueError("url must be include https://en.wikipedia.org/wiki/")
    @property
    def _file_name(self):
        return TEMP_FILE+ self.keyword + ".pdf"

    def download_pdf(self):
        download_url = DOWNLOAD_PREFIX + self.keyword
        print(download_url)
        req = requests.get(download_url,allow_redirects=True)
        print(req.content)
        path = default_storage.save(self._file_name,
                                    ContentFile(req.content))
        print(path)
        # open(self._file_name,"wb").write(req.content)

        return path, self.keyword+".pdf"


# w=WikipediaController("https://en.wikipedia.org/wiki/Sinhala_language")
# x = w.download_pdf()
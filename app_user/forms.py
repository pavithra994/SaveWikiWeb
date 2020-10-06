from django import forms


class Upload(forms.Form):
    # file = forms.FileField()
    wiki = forms.URLField(widget=forms.URLInput(attrs={'class':"form-control",
                                                       'placeholder':"Enter the Wikipedia URL"}
                                                ))
from django import forms

class joinform(forms.Form):
    username = forms.CharField(max_length=25,required=True)
    roomname = forms.CharField(max_length=25,required=True)
    
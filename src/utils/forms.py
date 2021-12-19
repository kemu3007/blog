from django import forms


class RakutenForm(forms.Form):
    pdf = forms.FileField(label="pdf")


class MUFJForm(forms.Form):
    pdf = forms.FileField(label="pdf")

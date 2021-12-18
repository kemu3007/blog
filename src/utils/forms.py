from django import forms


class RakutenForm(forms.Form):
    pdf = forms.FileField(label="pdf")

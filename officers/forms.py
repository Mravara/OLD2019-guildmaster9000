from django import forms


class DecayForm(forms.Form):
    decay = forms.FloatField(required=True)

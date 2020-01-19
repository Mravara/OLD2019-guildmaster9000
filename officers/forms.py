from django import forms
from members.models import Character


class DecayForm(forms.Form):
    decay = forms.FloatField(required=True)


class NewMemberForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    character_name = forms.CharField(required=True)
    character_class = forms.ChoiceField(choices=Character.MemberClass.choices)
    discord_id = forms.IntegerField(required=True)
    starting_ep = forms.IntegerField(required=True)
    starting_gp = forms.IntegerField(required=True)

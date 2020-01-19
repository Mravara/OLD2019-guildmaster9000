from django import forms
from items.models import Item, ItemInfo
from dungeons.models import Dungeon
from members.models import Character
from raid.models import RaidCharacter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.layout import Submit


class NewRaidForm(forms.Form):
    dungeon = forms.ModelChoiceField(
        queryset=Dungeon.objects.all(),
        label="Please choose a dungeon:",
        initial='1',
        )

    members = forms.CharField(widget=forms.Textarea)
    benched_members = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(NewRaidForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.label_class = 'float-left'


class GiveItemForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=RaidCharacter.objects.all(),
        label="",
        required=True
        )
    item = forms.CharField(label='', required=True)
    item_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    item_slot = forms.ModelChoiceField(queryset=ItemInfo.objects.all(), label='', initial=1)
    price = forms.FloatField(label='', initial='100', min_value=0, max_value=100, required=True)
    comment = forms.CharField(label='', required=False)


class GiveEPForm(forms.Form):
    character = forms.ModelChoiceField(queryset=RaidCharacter.objects.all(), required=False)
    only_present = forms.BooleanField(required=False)
    ep = forms.IntegerField(required=True)


class AddRaidersForm(forms.Form):
    character = forms.ModelChoiceField(queryset=Character.objects.all(), required=False)
    members = forms.CharField(required=False, widget=forms.Textarea)


class AddBenchedRaidersForm(forms.Form):
    character = forms.ModelChoiceField(queryset=Character.objects.all(), required=False)
    members = forms.CharField(required=False, widget=forms.Textarea)

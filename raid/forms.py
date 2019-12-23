from django import forms
from dungeons.models import Dungeon
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class NewRaidForm(forms.Form):
    dungeon = forms.ModelChoiceField(
        queryset=Dungeon.objects.all(),
        label="Please choose a dungeon:",
        initial='1',
        )

    def __init__(self, *args, **kwargs):
        super(NewRaidForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.label_class = 'float-left'
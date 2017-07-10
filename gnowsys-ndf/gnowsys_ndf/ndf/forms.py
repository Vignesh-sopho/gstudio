import datetime
import json
from django import forms
from django_mongokit.forms import DocumentForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

from models import Node
from models import GSystemType

from registration.forms import RegistrationForm
from passwords.fields import PasswordField

CHOICES=[("all",'All'),("Author",'Users'),("image",'Images'),("video",'Video'),("text",'Text'),("audio","Audio"),("Page",'Page'),("Group",'Courses')]
GROUP_CHOICES=[]
GROUP_CHOICES.append(("all","All"))
SEARCH_CHOICE = [(0,'Search for Data'),(1,'Contributions of an Author')]
group_map = {}

mapping_directory = '/home/docker/code/gstudio/gnowsys-ndf/gnowsys_ndf/ndf/mappings'

with open(mapping_directory+"/groupmap.json", 'r') as gm:
    group_map = json.load(gm)

for l in group_map.keys():
    tup = (l, group_map[l])
    tup = tuple(tup)
    GROUP_CHOICES.append(tup)

class SearchForm(forms.Form):
    query = forms.CharField(label = '', widget = forms.TextInput(attrs={'placeholder': 'Search for'}), error_messages = False)
    group = forms.ChoiceField(label = "Group", widget = forms.Select, choices = GROUP_CHOICES)
    select = forms.ChoiceField(label = "Filter", widget = forms.Select, choices = CHOICES)
    search_select = forms.ChoiceField(label = "Search for", widget = forms.Select(attrs={'placeholder': 'Search for'}), choices = SEARCH_CHOICE)
class NodeForm(DocumentForm):

    tags = forms.CharField(max_length=250)
    
    def clean_tags(self):
        value = self.cleaned_data['tags']
        return [tag.strip() for tag in value.split(',')]

    class Meta:
        document = Node
        fields = ['name', 'member_of', 'tags']
        
class UserRegistrationForm(RegistrationForm):
    password1 = PasswordField(label="Password")

class UserChangeform(PasswordChangeForm):
    new_password1 = PasswordField(label="New password") 

class UserResetform(SetPasswordForm):
    new_password1 = PasswordField(label="New password")

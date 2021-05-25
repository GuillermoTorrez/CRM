from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        # fields = '__all__'
        fields = (
           'first_name',
           'last_name',
           'age',
           'agent',
           'description',
           'phone_number',
           'email',
        )
        

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=18)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        fields_classes = {'username':UsernameField}

class AssignAgentForm(forms.Form):
    #agent = forms.ChoiceField(choices=(
    #    ('Agent 1', "Agent 1 Agent Full name"),
    #    ('Agent 2', "Agent 2 Agent Full name"),
    #))

    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        # print(request.user)
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )
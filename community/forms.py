from django import forms
from django.forms import ModelForm

from league.models import User

from machina.models.fields import MarkupTextFieldWidget

from .models import Community


class AdminCommunityForm(ModelForm):
    class Meta:
        model = Community

        fields = [
            'name',
            'slug',
            'description',
            'private_description',
            'close',
            'private',
            'promote'
        ]
        widgets = {
            'description': MarkupTextFieldWidget(attrs={'placeholder': 'Public description of the community.'}),
            'private_description': MarkupTextFieldWidget(attrs={'placeholder': 'Only community members can see it.'},)
        }

        help_texts = {
            'name': "Name of the community",
            'slug': "Short slug to identify the community. URL will be https://openstudyroom.org/community/slug/",
            'close': "If close, it's invitation only community. Otherwise, anyone can join.",
            'private': "If private, only members can see the community.",
            'promote': "If promoted, it's leagues will be shown to everyone in leagues views (same as OSR leagues)."
        }


class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = [
            'description',
            'private_description',
            'close',
            'private'
        ]

        widgets = {
            'description': MarkupTextFieldWidget(attrs={'placeholder': 'Public description of the community.'}),
            'private_description': MarkupTextFieldWidget(attrs={'placeholder': 'Only community members can see it.'},)
        }

        help_texts = {
            'close': "If close, it's invitation only community. Otherwise, anyone can join.",
            'private': "If private, only members can see the community.",
        }


class CommunytyUserForm(forms.Form):
    username = forms.CharField(label='username')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username__iexact=username).exists():
            message = "We don't have a user with username" + username + "."
            raise forms.ValidationError(message)
        return username

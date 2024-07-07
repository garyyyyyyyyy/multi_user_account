from django import forms

class CustomUserCreationForm(forms.Form):
    CHOICES = [
        ('district_office', 'District Office'),
        ('branch_location', 'Branch Location'),
    ]
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    access_level = forms.ChoiceField(choices=CHOICES)

class CustomUserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
from django import forms

class SearchForm(forms.Form):
    typeChoices = [('TAGS','Tags'), ('ARTICLES','Articles'), ('AUTHORS','Authors'), ('PUBLICATIONS', 'Publications'), ('PUBLISHERS','Publishers'), ('ALL','All')]
    searchTerm = forms.CharField(label='Search Term', max_length=100,required=False)
    searchModel = forms.ChoiceField(label='Area to Search', choices=typeChoices)
    fuzzySearch = forms.BooleanField(label='Fuzzy Search',required=False)

class AddTagForm(forms.Form):
    tagName = forms.CharField(label='Tag', max_length=100)
    tagDescriptor = forms.CharField(label='Description', max_length=100,required=False)

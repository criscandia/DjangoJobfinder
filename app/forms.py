from django import forms
from app.models import RSSFeed, Job

class JobSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, label='Keyword')
    company = forms.CharField(max_length=100, required=False, label='Company')
    location = forms.CharField(max_length=100, required=False, label='Location')
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget(), label='Start Date')
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget(), label='End Date')
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('Start date must be before end date')
        
        return cleaned_data

class RssFeedForm(forms.ModelForm):
    class Meta:
        model = RSSFeed
        fields = ['title', 'site_name', 'url']




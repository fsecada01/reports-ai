from django import forms
from .models import ReportInstance

class ReportInstanceForm(forms.ModelForm):
    class Meta:
        model = ReportInstance
        fields = ['title', 'report_type', 'git_repo_url']
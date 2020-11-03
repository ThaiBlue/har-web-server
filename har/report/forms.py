from django.forms import ModelForm
from .models import Report

# create report form
class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['user', 'name', 'latitude', 'longitude', 'altitude', 'accuracy']
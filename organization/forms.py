from django import forms
from organization.models import Organization, Office
from django.forms import modelformset_factory


class OrganizationSetupForm(forms.Form):
    '''
    Form to setup an Organization
    '''
    organization_name = forms.CharField(max_length=60, help_text='Required. Enter the name of your organization')

    class Meta:
        model = Organization
        fields = ("organization",)

    def clean_organization_name(self):
        '''
		Checks that there is not an existing organization with the same name
		'''
        organization_name_input = self.cleaned_data.get('organization_name')
        if Organization.objects.filter(organization_name=organization_name_input).exists():
            raise forms.ValidationError(
                "An Organizations is already registered with this name. Please choose another name.")
        return organization_name_input

# class OfficeSetupForm(forms.Form):
#     '''
#     Form to setup Offices after registration
#     '''
#     office_name = forms.CharField(max_length=50)
#     # TODO change location later to Google Maps thingy
#     office_location = forms.CharField(max_length=50)
#     office_capacity = forms.IntegerField()
#
#     class Meta:
#         model = Office
#         fields = ("office_name", "office_location", "office_capacity")

OfficeSetupFormSet = modelformset_factory(
    Office, fields=("office_name", "office_location", "office_capacity"), extra=3
)

BirdFormSet = modelformset_factory(
    Office, fields=("office_name", "office_location", "office_capacity"), extra=1
)
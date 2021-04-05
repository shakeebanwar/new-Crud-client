from django import forms
from overview.models import Booking
from django.utils import timezone


class BookingForm(forms.Form):
	booking_date = forms.DateTimeField()

	class Meta:
		# model = Booking
		# fields = ('id', 'booking_time', 'location', 'account_id', 'organization_id', 'office_id')
		model = Post
		# exclude = ['author', 'updated', 'created', ]
		fields = ['text']
		widgets = {
			'text': forms.TextInput(attrs={
				'id': 'post-text',
				'required': True,
				'placeholder': 'Say something...'
			}),
		}

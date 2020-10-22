from django import forms
from .models import Comment

# Form to filte the results of the melodies
class FilterForm(forms.Form):

	# Options of filter
	FILTERS = (
		('score', 'Score'),
		('aimodel', 'Model'),
		('bpm', 'Bpm'),
		('date_created', 'Date')
	)

	# Options for the order
	ORDERS = (
		('-', 'Descending'),
		('plus', 'Ascending')
	)

	m_filter = forms.ChoiceField(choices=FILTERS)
	m_order = forms.ChoiceField(choices=ORDERS)

# Form to send comments
class CommentForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['comment'].label = False
		self.fields['comment'].widget = forms.Textarea(attrs={"rows": 2, "cols": 25, "placeholder": "Use markdown language"})

	class Meta:
		model = Comment
		fields = ['comment']
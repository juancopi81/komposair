from django import forms

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

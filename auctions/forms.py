from django import forms
from .models import Bid, Comment

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-2'
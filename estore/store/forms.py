from django import forms
from  .models import ReviewRatings
class ReviewForms(forms.ModelForm):
    class Meta:
        model = ReviewRatings
        fields = ['subject', 'review', 'rating', ]
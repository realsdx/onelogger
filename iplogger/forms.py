from django import forms

class TrackingCodeForm(forms.Form):
    tracking_code = forms.CharField(label = 'Tracking Code', max_length=256, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter the Tracking Code'
        }
    ))
    

from django.forms import ModelForm
from .models import Imagine, Room,  Prescription
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']


class UploadForm(ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
        exclude = ['user','created']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class ImageForm(ModelForm):
    class Meta:
        model = Imagine
        fields = ['imge']
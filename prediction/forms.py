from django import forms
from .models import Employee, Doc, Patient


class OwnerReg(forms.Form):
    HospitalName = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form.control'}))
    OwnerName = forms.CharField(required=True, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    Email = forms.CharField(required=True, max_length=20, widget=forms.EmailInput(
        attrs={'class': 'form.control'}))
    MobNo = forms.RegexField(regex=r'^\+?1?\d{10,10}$')
    Password = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))
    ConfPasswd = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))


class OwnerLogin(forms.Form):
    Email = forms.CharField(required=False, max_length=20, widget=forms.EmailInput(
        attrs={'class': 'form.control'}))
    Password = forms.CharField(required=False, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))


class DocReg(forms.Form):
    OpUserName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    PasswordOp = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))
    ConfPasswdOp = forms.CharField(
        required=True, max_length=20, widget=forms.PasswordInput(attrs={'class': 'form.control'}))
    OpImage = forms.ImageField(required=True)

    LabUserName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    PasswordLab = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))
    ConfPasswdLab = forms.CharField(
        required=True, max_length=20, widget=forms.PasswordInput(attrs={'class': 'form.control'}))
    LabImage = forms.ImageField(required=True)

    DocUserName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    PasswordDoc = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))
    ConfPasswdDoc = forms.CharField(
        required=True, max_length=20, widget=forms.PasswordInput(attrs={'class': 'form.control'}))
    DocImage = forms.ImageField(required=True)
    DocNumber = forms.RegexField(regex=r'^\+?1?\d{10,10}$')


class OpLogin(forms.Form):
    OpUserName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    OpPassword = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))


class LabLogin(forms.Form):
    LabUserName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    LabPassword = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))


class DocLogin(forms.Form):
    DocUserName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    DocPassword = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form.control'}))


YEARS = [x for x in range(1980, 2022)]


class OpPatientReg(forms.Form):
    Name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form.cortrol'}))
    Age = forms.CharField(required=True, max_length=3, widget=forms.TextInput(
        attrs={'class': 'form.control'}))
    DateOfBirth = forms.DateField(
        initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))
    BloodGroup = forms.CharField(required=True, max_length=3)
    Place = forms.CharField(required=True, max_length=40, widget=forms.Textarea(
        attrs={'class': 'form.control', 'style': 'height:110px'}))
    PhoneNumber = forms.RegexField(regex=r'^\+?1?\d{10,10}$')
    PatientImage = forms.ImageField(required=True)


class OpPatientUpdate(forms.ModelForm):
    class Meta():
        model = Patient
        ordering = ['Name']
        fields = ('Name', 'Age', 'Place', 'PhoneNumber',
                  'DateOfBirth', 'BloodGroup')


CHOICES = [('pneumonia', 'pneumonia'), ('o', 'o')]


class LabPatientUpdate(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('ScanType',)
        AGE_CHOICES = (
            ('Select', 'Select'),
            ('Pneumonia', 'Pneumonia'),
            ('Corona', 'Corona'),
        )
        widgets = {'ScanType': forms.Select(choices=AGE_CHOICES, attrs={
                                            'class': 'form-control'}), }


class DocPatientDetails(forms.Form):
    LabUserName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form.control'}))

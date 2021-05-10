from prediction.encryption_util import *
import os
import gc
import cv2
import glob
import time
import torch
import imgkit
import torchvision
import torch.nn as nn
from PIL import Image
from datetime import date
import torch.nn.functional as F
import torchvision.models as models
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib import messages, auth
from torchvision.transforms import ToTensor
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from passlib.hash import des_crypt as resolver
from passlib.hash import pbkdf2_sha256 as Xsvaes
from django.views.decorators.csrf import csrf_exempt
from .models import Employee, Doc, Patient, News, Brain, Comments, Drugs
from .forms import DocPatientDetails, OwnerReg, DocReg, OpPatientReg, OpLogin, LabLogin, DocLogin, OwnerLogin, LabPatientUpdate, OpPatientUpdate
device = torch.device('cpu')


class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = models.resnet50(pretrained=True)
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Sequential(nn.BatchNorm1d(num_ftrs),
                                        nn.Linear(num_ftrs, 512),
                                        nn.ReLU(),
                                        nn.Dropout(.5),
                                        nn.Linear(512, 512),
                                        nn.ReLU(),
                                        nn.Linear(512, 2))

    def forward(self, xb):
        return torch.sigmoid(self.network(xb))


def to_device(data, device):
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)


def Index(request):

    if request.method == 'POST':
        Name = request.POST['name']
        Email = request.POST['email']
        Message = request.POST['message']
        obj = Comments(Name=Name, Email=Email, Message=Message)
        obj.save()

    return render(request, 'index.html')


def Contact(request):
    return render(request, 'contact.html')


def E256(strings):
    e256_string = Xsvaes.hash(strings, rounds=12000, salt_size=32)
    return e256_string


def D256(strings, enc_string):
    d256_string = Xsvaes.verify(strings, enc_string)
    return d256_string


def mSignup(request):
    if request.method == 'POST':
        form = OwnerReg(request.POST)

        if form.is_valid():
            table = Employee()

            table.HospitalName = form.cleaned_data['HospitalName']
            table.OwnerName = form.cleaned_data['OwnerName']
            table.Email = form.cleaned_data['Email']
            table.MobNo = form.cleaned_data['MobNo']
            passwd = form.cleaned_data['Password']
            passwd2 = form.cleaned_data['ConfPasswd']
            checking = Employee.objects.filter(Email=table.Email).exists()

            if checking:
                msg = "email already exist"
                args = {'form': form, 'error': msg}
                return render(request, 'signup.html', args)
            elif(passwd != passwd2):
                msg = "password mismatch"
                args = {'form': form, 'error': msg}
                return render(request, 'signup.html', args)
            else:
                table.Password = E256(passwd)
                table.ConfPasswd = E256(passwd2)
                table.save()
                return redirect('/mlogin')
    else:
        form = OwnerReg()
    return render(request, 'signup.html', {'form': form})


def mLogin(request):
    if request.method == 'POST':
        form = OwnerLogin(request.POST)
        if form.is_valid():
            Email = form.cleaned_data['Email']
            Passwd = form.cleaned_data['Password']
            checking = Employee.objects.all().filter(Email=Email)
            for enc in checking:
                value = D256(Passwd, enc.Password)
                if value != False:
                    for check in checking:
                        request.session['id'] = check.id
                        request.session['email'] = check.Email
                        return redirect('/home/%s' % check.id)
            else:
                return redirect('/mlogin/')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = OwnerLogin()
    return render(request, 'login.html', {'form': form})


def Logout(request):
    logout(request)
    return redirect('/')


def Home(request, id):
    if request.session.has_key:
        email = request.session['email']
        uid = request.session['id']
        user = Employee.objects.get(id=id)
        ur = Employee.objects.get(Email=email)
        news = News.objects.all()
        doc = Doc.objects.all()
        return render(request, 'news.html', {'user': user, 'ur': ur, 'news': news, 'doc': doc})


def Single(request, id):
    news = News.objects.get(id=id)
    newz = News.objects.all()

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    today = date.today()
    dt = today.strftime("%b-%d-%Y")

    return render(request, 'single.html', {'news': news, 'newz': newz})


def DocPage(request, id):
    if request.session.has_key:
        user = Employee.objects.get(id=id)
        em = Employee.objects.all()
        doc = Doc.objects.all()
    return render(request, 'doc.html', {'user': user, 'doc': doc, 'em': em, })


def Dreg(request, id):
    if request.session.has_key:
        user = Employee.objects.get(id=id)
        doc = Doc.objects.all()

        if request.method == 'POST':
            form = DocReg(request.POST or None, request.FILES)

            if form.is_valid():
                table = Doc()

                table.OpUserName = form.cleaned_data['OpUserName']

                table.PasswordOp = form.cleaned_data['PasswordOp']

                table.ConfPasswdOp = form.cleaned_data['ConfPasswdOp']
                table.OpImage = form.cleaned_data['OpImage']

                table.LabUserName = form.cleaned_data['LabUserName']
                table.PasswordLab = form.cleaned_data['PasswordLab']
                table.ConfPasswdLab = form.cleaned_data['ConfPasswdLab']
                table.LabImage = form.cleaned_data['LabImage']

                table.DocUserName = form.cleaned_data['DocUserName']
                table.PasswordDoc = form.cleaned_data['PasswordDoc']
                table.ConfPasswdDoc = form.cleaned_data['ConfPasswdDoc']
                table.DocImage = form.cleaned_data['DocImage']

                table.DocNumber = form.cleaned_data['DocNumber']
                table.Redirect_id_doc = id

                if (Doc.objects.filter(OpUserName=table.OpUserName).exists()):
                    msg = "Opuser name already exist"
                    args = {'form': form, 'error': msg, 'user': user}
                    return render(request, 'docreg.html', args)

                elif table.PasswordOp != table.ConfPasswdOp:
                    msg = "password mismatch"
                    args = {'form': form, 'error': msg, 'user': user}
                    return render(request, 'docreg.html', args)

                elif (Doc.objects.filter(DocNumber=table.DocNumber).exists()):
                    msg = "try unique"
                    args = {'form': form, 'error': msg, 'user': user}
                    return render(request, 'docreg.html', args)

                elif (Doc.objects.filter(LabUserName=table.LabUserName).exists()):
                    msg = "Labuser name already exist"
                    args = {'form': form, 'error': msg, 'user': user}
                    return render(request, 'docreg.html', args)
                elif table.PasswordLab != table.ConfPasswdLab:
                    msg = "password mismatch"
                    args = {'form': form, 'error': msg, 'user': user}
                    return render(request, 'docreg.html', args)

                elif (Doc.objects.filter(DocUserName=table.DocUserName).exists()):
                    msg = "Docuser name already exist"
                    args = {'form': form, 'error': msg, 'user': user}
                    return render(request, 'docreg.html', args)
                elif table.PasswordDoc != table.ConfPasswdDoc:
                    msg = "password mismatch"
                    args = {'form': form, 'error': msg, 'user': user}
                    return render(request, 'docreg.html', args)
                else:
                    table.save()
                    return redirect('/home/%s' % user.id)
        else:
            form = DocReg()
        return render(request, 'docreg.html', {'form': form, 'user': user, 'doc': doc})


def Op(request, id):
    print('op door')
    if request.session.has_key:
        user = Employee.objects.get(id=id)
        doc = Doc.objects.all()
        ur = Patient.objects.all()
        if request.method == 'POST':
            form = OpLogin(request.POST)
            if form.is_valid():
                username = form.cleaned_data['OpUserName']
                passwd = form.cleaned_data['OpPassword']
                checking = Doc.objects.all().filter(OpUserName=username, PasswordOp=passwd)
                for check in checking:
                    request.session['id'] = check.id
                    request.session['OpUserName'] = check.OpUserName

                    return redirect('/ophome/%s' % check.id)
                else:
                    return HttpResponse('error')
            else:
                print(form.error)
                return render(request, 'op.html', {'form': form, 'user': user})
        else:
            form = OpLogin()
        return render(request, 'op.html', {'form': form, 'user': user, })


def OpHome(request, id):
    print('ophome door')
    if request.session.has_key:
        users = Doc.objects.get(id=id)
        ur = Patient.objects.all()
        doc = Doc.objects.all()
        d = Doc.objects.get(id=id)
        hospital = Employee.objects.get(id=users.Redirect_id_doc)
        if request.method == 'POST':
            form = OpPatientReg(request.POST or None, request.FILES)
            if form.is_valid():
                table = Patient()

                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)

                today = date.today()
                dt = today.strftime("%b-%d-%Y")

                print('current time::', current_time)

                table.Name = form.cleaned_data['Name']
                table.Age = form.cleaned_data['Age']
                table.DateOfBirth = form.cleaned_data['DateOfBirth']
                BloodGroup = form.cleaned_data['BloodGroup']
                table.BloodGroup = BloodGroup.capitalize()
                table.Place = form.cleaned_data['Place']
                table.PhoneNumber = form.cleaned_data['PhoneNumber']
                table.PatientImage = form.cleaned_data['PatientImage']

                table.DocNumber = users.DocNumber
                table.DocName = users.DocUserName

                table.Redirect_id = id
                table.HospitalName = hospital.HospitalName
                table.HospitalEmail = hospital.Email
                table.OpName = d.OpUserName
                table.HospitalNumber = hospital.MobNo
                table.Time = current_time
                table.Date = dt

                table.save()
                messages.success(request, 'Form submission successful')
                return redirect('/ophome/%s' % id)
        else:
            form = OpPatientReg()
        return render(request, 'ophome.html', {'ur': ur, 'form': form, 'user': users, 'doc': doc, 'hospital': hospital})


def OpEdit(request, id):
    if request.session.has_key:
        user = Patient.objects.get(id=id)
        ur = Patient.objects.all()
        doc = Doc.objects.all()

        data = Patient.objects.all()
        if request.method == 'POST':
            form = OpPatientUpdate(request.POST or None, instance=user)
            if form.is_valid():
                rid = request.POST.get('Rid')

                form.save()
                return redirect('/ophome/%s' % user.Redirect_id)
        else:
            form = OpPatientUpdate(request.POST or None, instance=user)
        return render(request, 'opedit.html', {'form': form, 'user': user, 'ur': ur, 'doc': doc})


def Lab(request, id):
    if request.session.has_key:
        user = Employee.objects.get(id=id)
        doc = Doc.objects.all()
        if request.method == 'POST':
            form = LabLogin(request.POST)

            if form.is_valid():
                username = form.cleaned_data['LabUserName']
                passwd = form.cleaned_data['LabPassword']

                checking = Doc.objects.all().filter(LabUserName=username, PasswordLab=passwd)

                for check in checking:
                    request.session['id'] = check.id
                    request.session['LabUserName'] = check.LabUserName

                    return redirect('/labhome/%s' % check.id)
                else:
                    return HttpResponse('error')
            else:

                return render(request, 'lab.html', {'form': form, 'user': user})

        else:
            form = LabLogin()
        return render(request, 'lab.html', {'form': form, 'user': user, 'doc': doc})


def LabHome(request, id):
    if request.session.has_key:
        users = Doc.objects.get(id=id)
        ur = Patient.objects.all()
        return render(request, 'labhome.html', {'ur': ur, 'user': users})


def LabEdit(request, id):
    if request.session.has_key:
        user = Patient.objects.get(id=id)
        ur = Patient.objects.all()
        doc = Doc.objects.all()

        data = Patient.objects.all()

        if request.method == 'POST':
            table = user
            rid = request.POST.get('Rid')
            uploadxray = request.FILES.get('uploadxray')
            table.XrayImage = uploadxray
            table.save()
            namexray = str(table.XrayImage)
            imgo = os.path.splitext(namexray)
            form = LabPatientUpdate(request.POST)

            if form.is_valid():
                scantype = form.cleaned_data['ScanType']
                table.ScanType = scantype
            url = os.path.join(
                r'/home/hades/Desktop/Cibernetico/media/', namexray)

            if scantype == 'Pneumonia':
                brain = r"/home/hades/Desktop/xray.pth"

                data = torch.load(brain, map_location=torch.device('cpu'))
                data['model_stat']
                model_state = data['model_stat']

                model1 = CNN().to(device)
                model1.load_state_dict(model_state)
                model1.eval()
                ximg = url

                image = cv2.imread(ximg, 1)

                bigger = cv2.resize(image, (128, 128))
                img = ToTensor()(bigger)
                xb = to_device(img.unsqueeze(0), device)

                yb = model1(xb)
                _, pred = torch.max(yb, dim=1)

                if pred == 1:
                    user.GeneratedResult = 'Positive(+ve)'

                elif pred == 0:
                    user.GeneratedResult = 'Negative(-ve)'
                else:
                    user.GeneratedResult = 'Server Error'
                table.save()
                return redirect('/labhome/%s' % rid)

            elif scantype == 'Corona':
                brain = r"/home/hades/Desktop/xray.pth"

                data = torch.load(brain, map_location=torch.device('cpu'))
                data['model_stat']
                model_state = data['model_stat']

                model1 = CNN().to(device)
                model1.load_state_dict(model_state)
                model1.eval()
                ximg = url

                image = cv2.imread(ximg, 1)

                bigger = cv2.resize(image, (128, 128))
                img = ToTensor()(bigger)
                xb = to_device(img.unsqueeze(0), device)

                yb = model1(xb)
                _, pred = torch.max(yb, dim=1)

                if pred == 1:
                    user.GeneratedResult = 'Positive(+ve)'

                elif pred == 0:
                    user.GeneratedResult = 'Negative(-ve)'
                else:
                    user.GeneratedResult = 'Server Error'
                table.save()
                return redirect('/labhome/%s' % rid)

        else:
            form = LabPatientUpdate(request.POST or None, instance=user)

        return render(request, 'labedit.html', {'form': form, 'user': user, 'ur': ur, 'doc': doc})


def Dlogin(request, id):
    print('Dlogin')
    if request.session.has_key:
        user = Employee.objects.get(id=id)
        doc = Doc.objects.all()
        if request.method == 'POST':

            form = DocLogin(request.POST)
            if form.is_valid():

                username = form.cleaned_data['DocUserName']
                passwd = form.cleaned_data['DocPassword']
                checking = Doc.objects.all().filter(DocUserName=username, PasswordDoc=passwd)

                for check in checking:
                    request.session['id'] = check.id
                    request.session['DocUserName'] = check.DocUserName
                    return redirect('/dochome/%s' % check.id)
                else:
                    return HttpResponse('error')
            else:
                return render(request, 'doclogin.html', {'form': form, 'user': user, 'doc': doc})
        else:

            form = DocLogin()
        return render(request, 'doclogin.html', {'form': form, 'user': user, 'doc': doc})


def DocHome(request, id):
    if request.session.has_key:
        users = Doc.objects.get(id=id)
        ur = Patient.objects.all()
        return render(request, 'dochome.html', {'ur': ur, 'user': users})


def DocEdit(request, id):
    if request.session.has_key:
        user = Patient.objects.get(id=id)

        ur = Patient.objects.all()
        doc = Doc.objects.all()
        drug = Drugs.objects.all()

        if request.method == 'POST':
            table = user
            dr = request.POST['docresult']
            table.DocResult = dr
            table.save()
            return redirect('/dochome/%s' % user.Redirect_id)
        else:
            form = DocPatientDetails(request.POST or None)
        return render(request, 'docedit.html', {'form': form, 'user': user, 'ur': ur, 'doc': doc, 'drug': drug})


def PrintOut(request, id):
    user = Patient.objects.get(id=id)
    # imgkit.from_file('print.html', 'out.jpg')        # HTML to JPG Converter (Not working)
    return render(request, 'print.html', {'user': user})

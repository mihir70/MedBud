from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . models import Message, Prescription, Room,Topic, Imagine
from . forms import RoomForm, UserForm,UploadForm, ImageForm
import os
@login_required(login_url='login')  ##
def home(request):
    q = request.GET.get('q')
    if q!=None:
        rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
        room_messages=Message.objects.filter(room__topic__name__icontains=q)
    else:
        rooms=Room.objects.all()
        room_messages=Message.objects.all()
    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'messages':room_messages}
    return render(request,'base/home.html',context)

@login_required(login_url='login')   ##
def room(request,pk):
    if Room.objects.filter(id=pk).exists()==False:
        return HttpResponse('Room DoesNot exist')
    rom=Room.objects.get(id=pk)
    msg=rom.message_set.all().order_by('-created')
    participants=rom.participants.all()
    if request.method == 'POST':
        body= request.POST.get('body')
        message=Message.objects.create(user = request.user,room = rom, body = body)
        rom.participants.add(request.user)
        return redirect('room',pk=rom.id)

    return render(request,'base/room.html',{'room':rom,'msg':msg,'participants':participants})

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=="POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,topic=topic,name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    if Room.objects.filter(id=pk).exists()==False:
        return HttpResponse('Room does not exist')
    room=Room.objects.get(id=pk)
    topics=Topic.objects.all()
    form=RoomForm(instance=room)
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('room',pk)
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    if Room.objects.filter(id=pk).exists()==False:
        return HttpResponse('Room Does Not exist')
    room=Room.objects.get(id=pk)
    if(request.method=="POST"):
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User Doesnot Exist')
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Details')
    context={'page':'login'}
    return render(request,'base/login_register.html',context)

@login_required(login_url='login') ##
def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='regis'
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            form.save()
            Imagine.objects.create(user=user)
            login(request,user)
            
            return redirect('home')
        else:
            messages.error(request,'Username already exists or Invalid details')

    context={'form':form,'page':page}
    return render(request,'base/login_register.html',context)

@login_required(login_url='login')
def deleteMessage(request,pk):
    if Message.objects.filter(id=pk).exists()==False:
        HttpResponse('Message doesnot exist')
    msg=Message.objects.get(id=pk)
    if(request.method=="POST"):
        msg.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':msg})

@login_required(login_url='login')
def userProfile(request,pk):
    if User.objects.filter(id=pk).exists()==False:
        HttpResponse('User doesnot exist')
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateUser(request):
    user=request.user
    inst=request.user.imagine
    form=ImageForm(instance=inst)
    if request.method=="POST":
        form = ImageForm(request.POST,request.FILES,instance=inst)
        form.save()
        print("updated")
        return redirect('profile',pk=user.id)
    return render (request,'base/update-user.html',{'form':form})

@login_required(login_url='login') ##
def topicPage(request):
    q = request.GET.get('q')
    if q!=None:
        topics=Topic.objects.filter(Q(name__icontains=q))
    else:
        topics=Topic.objects.all()
    
    context={'topics':topics}
    return render(request,'base/topics.html',context)

@login_required(login_url='login') ##
def activityPage(request):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,'base/activity.html',context)

@login_required(login_url='login')
def prescriptionPage(request):
    q = request.GET.get('q')
    if q!=None:
        rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
        room_messages=Message.objects.filter(room__topic__name__icontains=q)
    else:
        rooms=Room.objects.all()
        room_messages=Message.objects.all()
    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    usr=request.user
    prescriptions=usr.prescription_set.all()
    context={'prescriptions':prescriptions,'topics':topics,'messages':room_messages,'room_count':room_count}
    return render(request,'base/prescription.html',context)

@login_required(login_url='login')
def uploadPrescription(request):
    form=UploadForm()
    if request.method=='POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            frm=form.save(commit=False)
            frm.user=request.user
            frm.save()
            print("Saved")
            return redirect('prescriptions')
        else:
            print("invalid")
            messages.error(request,'Invalid details')

    context={'form':form}
    return render(request,'base/upload.html',context)

@login_required(login_url='login')
def deletePrescription(request,pk):
    if Prescription.objects.get(id=pk).exists()==False:
        return HttpResponse('404 Not Found')
    pres=Prescription.objects.get(id=pk)
    if(request.method=="POST"):
        os.remove(pres.img.path)
        pres.delete()
        return redirect('prescriptions')
    return render(request,'base/delete.html',{'obj':pres})
    

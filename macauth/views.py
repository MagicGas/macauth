from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse
from macauth.models import User
import json
from  macauth.models import MacAddr
from macauth.macoperation import mac_compare as cop,addmac,rmmac
# Create your views here.

def index(request):
    return redirect('/loginPage')

def loginPage(request):
    if request.COOKIES.get("loginsts",None)=='online':
        return redirect('/macauth')
    return render(request,"login.html")

def login(request):
    if request.method == 'POST':
        login_sts ={
            "status":"offline",
            'username':None
        }
        try:
            username = request.POST.get('user')
            password =request.POST.get('pass')
            if User.objects.filter(username=username, password=password).first():
                login_sts["status"]='online'
                login_sts["username"]=username
                response = HttpResponse(json.dumps(login_sts))
                response.set_cookie('loginsts','online',max_age=3600)
                return response
            else:
                return HttpResponse(json.dumps(login_sts))
        except :
            return HttpResponse(json.dumps(login_sts))

    else:
        return  redirect('/loginPage')


def macauth(request):
    if request.COOKIES.get("loginsts", None):
        return  render(request,'index.html')
    else:
        return redirect('/loginPage')

def showdata(request):
    if request.method == "POST":
        position = request.POST.get("position",None)
        macs = MacAddr.objects.filter(position=position).all()
        mac_group = []
        for item in macs:
            mac_group.append(item.macaddr)
        return HttpResponse(json.dumps(mac_group))
    else:
        return redirect('/loginPage')

def macedit(request):
    if request.method == "POST":
        position = request.POST.get("position",None)
        maclist = list(json.loads(request.POST.get("macdata",None)))
        macobj = MacAddr.objects.filter(position=position).all()

        if  macobj:
            oldlist = []
            for item in macobj:
                oldlist.append(item.macaddr)
            addlist,rmlist = cop(oldlist,maclist)
            result_add = addmac(position,addlist)
            result_rm = rmmac(position,rmlist)
            if result_add and result_rm:
                return HttpResponse("success")
            else:
                return HttpResponse("fail")
        else:
            print(maclist)
            result = addmac(position,maclist)
            if result:
                return HttpResponse("success")
            else:
                return HttpResponse("fail")
    else:
        return redirect('/loginPage')


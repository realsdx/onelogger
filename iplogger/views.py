from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from .forms import TrackingCodeForm
from .models import User,TrackingCode,Log
from random import randint
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
def index(req):
    if req.method == 'POST':
        tracking_code_form = TrackingCodeForm(req.POST)
        if tracking_code_form.is_valid():
            code_list = [c for c in TrackingCode.objects.all().values_list('code',flat=True)]
            #print("CODElist:"+str(code_list))
            t_code = int(tracking_code_form.cleaned_data['tracking_code'])
            #print("TCODE:"+str(t_code))
            if t_code in code_list:           
                print("Redirected to result")
                return HttpResponseRedirect('/results/'+str(t_code)+'/',{'tracking_code':t_code})
            else:
                print("F")
    else:
        tracking_code_form = TrackingCodeForm()

    return render(req,'iplogger/index.html',{'tracking_code_form':tracking_code_form})

def track(req, tracking_code):
    info = {}
    required_headers=['REMOTE_ADDR','HTTP_HOST','HTTP_USER_AGENT','HTTP_HOST','HTTP_REFERER']
    for keys in required_headers:
        info[keys]=req.META[keys]
    
    return render(req,'iplogger/track.html',{'ipinfo':info})


def results(req, tracking_code):
    #test for ip infoclear

    info = {}
    required_headers=['REMOTE_ADDR','HTTP_USER_AGENT','HTTP_HOST','HTTP_REFERER','HTTP_HOST']
    for keys in required_headers:
        try:
            info[keys]=req.META[keys]
        except KeyError:
            info[keys]='N/A'
    #print(info)
    #print("HOST::"+req.get_host())
    context={'tracking_code':tracking_code,'headers':info}
    return render(req,'iplogger/results.html',context)

def createlink(req):
    if(req.POST):
        code_list = [c for c in TrackingCode.objects.all().values_list('code',flat=True)]
        code = randint(1000000,9999999)
        while code in code_list:
            code = randint(1000000,9999999)
        print(code)
        return JsonResponse({'code':code})
    else:
        return render(req,'iplogger/createlink.html',{'code':''})

def register(req):
    if(req.POST):
        form = UserCreationForm(req.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/',{})
    else:
        form = UserCreationForm()
        return render(req, 'registration/register.html',{'form':form})
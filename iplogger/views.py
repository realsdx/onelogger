from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from iplogger.forms import TrackingCodeForm
from iplogger.models import TrackingCode, Log
from random import randint
from django.contrib.auth import get_user_model
from iplogger.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

import json
import traceback

#Django sucks here, Need to import the custom User model explicitly, even though u updated th settings
User = get_user_model()
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
    try:
        tracking_code = int(tracking_code)
        if TrackingCode.objects.filter(code=tracking_code).exists():
            info = {}
            required_headers = ['REMOTE_ADDR','HTTP_USER_AGENT','HTTP_HOST','HTTP_REFERER']
            for keys in required_headers:
                try:
                    info[keys]=req.META[keys]
                except KeyError:
                    info[keys]='N/A'
            #Save logs in any case (it may be same) and count hits
            json_info = json.dumps(info)
            #get the code_obj to link with foreign key
            code_obj = TrackingCode.objects.get(code=tracking_code)
            log_obj = Log(code=code_obj, headers_info=json_info)
            log_obj.save()        
            return render(req,'iplogger/track.html',{'headers':info})

        else:
            return None

    except Exception:
        traceback.print_exc()


@login_required
def results(req, tracking_code):
    code_obj = TrackingCode.objects.get(code=tracking_code)
    logs_obj_list = code_obj.log_set.all() #Get all objects using reference
    
    logs = {}
    for i,log in enumerate(logs_obj_list):
        logs.update({ i:json.loads(log.headers_info) })

    context={'tracking_code':tracking_code,'logs':logs}
    return render(req,'iplogger/results.html',context)

@login_required
def createlink(req):
    if(req.method == 'POST' and req.user.is_authenticated and 'gen_code' in req.POST):
        global code_to_save
        print(req.POST)
        code_list = [c for c in TrackingCode.objects.all().values_list('code',flat=True)]
        code = randint(1000000,9999999)
        while code in code_list:
            code = randint(1000000,9999999)
        print(code)
        code_to_save = code
        return JsonResponse({'code':code})

    elif(req.method == 'POST' and 'save_code' in req.POST):
        print(req.user)
        current_user = req.user#User.objects.get(username=req.user)
        if current_user.is_authenticated and (code_to_save != None):
            code_obj = TrackingCode(code=code_to_save, user=current_user)
            code_obj.save()
            print("Code saved:", code_to_save)
            #reset code to None
            code_to_save = None
            return JsonResponse({'res':'success'})
        else:
            return JsonResponse({'res':'error'})

    else:
        return render(req,'iplogger/createlink.html',{'code':''})

def register(req):
    if(req.POST):
        form = UserCreationForm(req.POST)
        if form.is_valid:
            #Begin reCAPTCHA validation
            form.save()
            return HttpResponseRedirect('/',{})
    else:
        form = UserCreationForm()
        return render(req, 'registration/register.html',{'form':form})

@login_required
def mylogs(req):
    
    return render(req, 'iplogger/mylogs.html',{})
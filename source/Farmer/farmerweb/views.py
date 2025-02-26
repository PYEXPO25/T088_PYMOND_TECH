from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
import requests
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password


@never_cache
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request=request, username=username, password=password,first_name="farmer")
        if user is not None:
            login(request, user)
            return redirect(reverse("farmerweb:dashboardpage"))
        else:
            messages.error(request, 'Invalid username or password')
            return redirect(reverse("farmerweb:loginpage"))
    return render(request,"farmerweb/index.html")

def home(request):
    return redirect(reverse("farmerweb:loginpage"))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password=request.POST.get('confirm')
        firstname="farmer"
        user_data_has_error = False
        
        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, 'Password must be at least 5 characters')
        if password!=confirm_password:
            user_data_has_error = True
            messages.error(request, 'Passwords Do Not Match')

        if not user_data_has_error:
            new_user = User.objects.create_user(
                email = email,
                username = username,
                password = password,
                first_name=firstname
            )
            messages.success(request, 'Account created. Login now')
            return redirect(reverse("farmerweb:loginpage"))
        else:
            return redirect(reverse("farmerweb:registerpage"))
    return render(request,"farmerweb/register.html")

@login_required
def dashboard(request):
    return render(request,"farmerweb/dashboard.html",{'active_page': 'dashboard'})

@login_required
def cropmanagement(request):
    if request.method=="POST":
        cropname=request.POST.get('Crop')
        farmername=request.user
        exist=Croplist.objects.filter(farmername_id=request.user)
        for data in exist:
            if data.cropname==cropname:
                messages.warning(request,f"The Crop {cropname} Already Exists")
                crops=Croplist.objects.filter(farmername_id=request.user)
                return render(request,"farmerweb/cropmanagement.html",{'active_page': 'cropmanagement',"crops":crops})
        messages.warning(request,f"The Crop {cropname} Is Added Successfully")
        add=Croplist(cropname=cropname,farmername=farmername)
        add.save()
    crops=Croplist.objects.filter(farmername_id=request.user)
    return render(request,"farmerweb/cropmanagement.html",{'active_page': 'cropmanagement',"crops":crops})

@login_required
def diseasecontrol(request):
    if request.method=="POST":
        cropname=request.POST.get('Crop')
        diseases=disease.objects.filter(cropname=cropname)
        crops=Croplist.objects.filter(farmername_id=request.user)
        return render(request,"farmerweb/diseasecontrol.html",{'active_page': 'disease','crops':crops,'diseases':diseases})
    crops=Croplist.objects.filter(farmername_id=request.user)
    return render(request,"farmerweb/diseasecontrol.html",{'active_page': 'disease','crops':crops})

@login_required
def weatherupdate(request):
        city = location.objects.filter(farmername_id=request.user)
        for data in city:
            city=data.Location
        api_key = "a0f54834d5c91887ed11a16398ec0c5f"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            return render(request, "farmerweb/weatherupdate.html", {"error": "City not found!", 'active_page': 'weather'})

        # Extract Weather Data
        temperature = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"] * 3.6  # Convert from m/s to km/h
        cloud_cover = response["clouds"]["all"]
        rain = response.get("rain", {}).get("1h", 0)  # Get rain amount in mm

        # **Irrigation Logic**
        irrigation_schedule = "Normal irrigation required."
        if temperature > 35 and humidity < 30:
            irrigation_schedule = "Increase irrigation by 20% due to high temperature and low humidity."
        elif temperature < 25 and humidity > 70:
            irrigation_schedule = "Decrease irrigation by 30% as temperature is low and humidity is high."
        elif wind_speed > 20:
            irrigation_schedule = "Water early morning or late evening to avoid evaporation."
        elif cloud_cover > 70:
            irrigation_schedule = "Reduce irrigation by 20% as cloud cover is high."
        elif rain > 5:
            irrigation_schedule = "Skip irrigation for today as rain is expected."

        weather_data = {
            "city": response["name"],
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "cloud_cover": cloud_cover,
            "rain": rain,
            "description": response["weather"][0]["description"],
            "irrigation_schedule": irrigation_schedule,
        }

        return render(request, "farmerweb/weatherupdate.html", {"weather": weather_data, 'active_page': 'weather'})
@login_required
def plantation(request):
    if request.method=="POST":
        tips=plantationtips.objects.filter(cropname=request.POST.get('Crop'))
        crops=Croplist.objects.filter(farmername_id=request.user)
        return render(request,"farmerweb/plantationtips.html",{'active_page': 'plantation',"crops":crops,"tips":tips})

    crops=Croplist.objects.filter(farmername_id=request.user)
    return render(request,"farmerweb/plantationtips.html",{'active_page': 'plantation',"crops":crops})

@login_required
def account(request):
    if request.method=="POST":
        if request.POST.get('Location'):
            Location=request.POST.get('Location')
            farmername=request.user
            exist=location.objects.filter(farmername_id=request.user)
            if not exist:
                add=location(Location=Location,farmername=farmername)
                add.save()
            else:
                exist=location.objects.filter(farmername_id=request.user).update(Location=Location)
        if request.POST.get('Phone'):
            Phone=request.POST.get('Phone')
            farmername=request.user
            exist=location.objects.filter(farmername_id=request.user)
            if not exist:
                add=location(phonenumber=Phone,farmername=farmername)
                add.save()
            else:
                exist=location.objects.filter(farmername_id=request.user).update(phonenumber=Phone)
    crops=Croplist.objects.filter(farmername_id=request.user)
    data=location.objects.filter(farmername_id=request.user)
    return render(request,"farmerweb/account.html",{'active_page': 'account','crops':crops,'datas':data})

@login_required
def fertilizers(request):
    if request.method=="POST":
        crop=request.POST.get('Crop')
        fertilizer=fertilizerss.objects.filter(cropname=crop)
        crops=Croplist.objects.filter(farmername_id=request.user)
        return render(request,"farmerweb/fertilizers.html",{'active_page': 'fertilizers','crops':crops,"fertilizers":fertilizer})
    crops=Croplist.objects.filter(farmername_id=request.user)
    return render(request,"farmerweb/fertilizers.html",{'active_page': 'fertilizers','crops':crops})


@login_required
def sellersite(request):
    if request.method=="POST":
        try:
            farmername=request.user
            detail=location.objects.filter(farmername_id=request.user)
            farmerlocation=""
            farmermobile=""
            for m in detail:
                farmerlocation=m.Location
                farmermobile=m.phonenumber
            cropname=request.POST.get('crop')
            quantity=request.POST.get('quantity')
            price=request.POST.get('price')
            experience=request.POST.get('experience')
            add=seller(cropname=cropname,quantity=quantity,price=price,experience=experience,farmername=farmername,farmermobile=farmermobile,farmerlocation=farmerlocation)
            add.save()
            messages.warning(request,f"The Crop {cropname} Is Added Successfully")
        except:
            messages.warning(request,f"Something Went Wrong")
    crops=Croplist.objects.filter(farmername_id=request.user)
    return render(request,"farmerweb/sellerpage.html",{'active_page': 'sellersite','crops':crops})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("farmerweb:loginpage"))

def ForgotPassword(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            # create a new reset id
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # creat password reset ur;
            password_reset_url = reverse('farmerweb:reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            # email content
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'

            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect(reverse('farmerweb:password-reset-sent', kwargs={'reset_id': new_password_reset.reset_id}))

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect(reverse('farmerweb:forgot-password'))
    return render(request, 'farmerweb/forgot_password.html')

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'farmerweb/password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect(reverse('farmerweb:forgot-password'))

def ResetPassword(request, reset_id):
    try:
        reset_id = PasswordReset.objects.get(reset_id=reset_id)
        if request.method == 'POST':

            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:

                # delete reset id if expired
                reset_id.delete()

                passwords_have_error = True
                messages.error(request, 'Reset link has expired')
            
            # reset password
            if not passwords_have_error:
                user = reset_id.user
                user.set_password(password)
                user.save()
                
                # delete reset id after use
                reset_id.delete()

                # redirect to login
                messages.success(request, 'Password reset.Proceed to login')
                return redirect(reverse("farmerweb:loginpage"))

            else:
                # redirect back to password reset page and display errors
                return redirect(reverse('farmerweb:reset-password', kwargs={'reset_id':reset_id}))
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect(reverse("farmerweb:forgot-password"))

    return render(request, 'farmerweb/reset_password.html')

def diseaseshow(request,diseasename):
    diseases=disease.objects.filter(diseasename=diseasename)
    return render(request,"farmerweb/diseaseshow.html",{'diseases':diseases})


def remove_crop(request, crop_id):
    crop = get_object_or_404(Croplist, id=crop_id)  
    crop_name = crop.cropname  
    crop.delete()
    messages.success(request, f"{crop_name} has been removed successfully!")
    return redirect(reverse("farmerweb:cropmanagementpage"))  

def merchantregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password=request.POST.get('confirm')
        firstname="merchant"
        user_data_has_error = False
        
        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, 'Password must be at least 5 characters')
        if password!=confirm_password:
            user_data_has_error = True
            messages.error(request, 'Passwords Do Not Match')

        if not user_data_has_error:
            new_user = User.objects.create_user(
                email = email,
                username = username,
                password = password,
                first_name=firstname
            )
            messages.success(request, 'Account created. Login now')
            return redirect(reverse("farmerweb:merchantloginpage"))
        else:
            return redirect(reverse("farmerweb:merchantregisterpage"))
    return render(request,"farmerweb/merchantregister.html")
    
def merchantlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password,first_name="farmer")
        if user is not None:
            login(request,user)
            return redirect(reverse("farmerweb:merchanthomepage"))
        else:
            messages.error(request, 'Invalid username or password')
            return redirect(reverse("farmerweb:merchantloginpage"))
    return render(request,"farmerweb/merchantlogin.html")

def merchantdashboard(request):
    sale=seller.objects.all()
    return render(request,"farmerweb/merchanthome.html",{'active_page': 'merchant_home','sales':sale})

def merchantaccount(request):
    if request.method=="POST":
        if request.POST.get('Location'):
            Location=request.POST.get('Location')
            farmername=request.user
            exist=location.objects.filter(farmername_id=request.user)
            if not exist:
                add=location(Location=Location,farmername=farmername)
                add.save()
            else:
                exist=location.objects.filter(farmername_id=request.user).update(Location=Location)
        if request.POST.get('Phone'):
            Phone=request.POST.get('Phone')
            farmername=request.user
            exist=location.objects.filter(farmername_id=request.user)
            if not exist:
                add=location(phonenumber=Phone,farmername=farmername)
                add.save()
            else:
                exist=location.objects.filter(farmername_id=request.user).update(phonenumber=Phone)
    data=location.objects.filter(farmername_id=request.user)
    return render(request,"farmerweb/merchantaccount.html",{'active_page': 'merchant_account','datas':data})

def merchantlogout(request):
    logout(request)
    return redirect(reverse("farmerweb:merchantloginpage"))

def scheme(request):
    schemess=schemes.objects.all()
    return render(request,"farmerweb/schemes.html",{'schemes':schemess})

def loann(request):
    loanss=loan.objects.all()
    return render(request,"farmerweb/loans.html",{'loans':loanss})
from django.shortcuts import render, HttpResponse, redirect
from Home.models import *
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth.hashers import *
# Create your views here.

def index(request):
    if("authenticated" in request.session.keys() and request.session["authenticated"]):
        username = request.session["username"]
        role = request.session["role"]
        user_data = Users.objects.filter(Username = username, Role = role).first()
        context = {}
        if(user_data):
            user_address = Address.objects.filter(Username_id = user_data.id).first()
            context["profile_image"]= str(user_data.Profile_Picture).replace("/static", "")
            context["user_userid"]= user_data.Username
            context["user_role"]= user_data.Role
            context["user_email"]= user_data.Email_id
            context["user_name"]= user_data.First_Name
            context["user_title"]= user_data.Last_Name
            context["user_line"]= user_address.Line
            context["user_city"]= user_address.city
            context["user_state"]= user_address.state
            context["user_pincode"]=user_address.pincode

        return render(request, "index.html", context)
    return redirect("/signin/")
def signin(request):
    if(request.method == 'POST'):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        user_data = Users.objects.filter(Username = username, Role = role).first()

        if(not user_data):
            messages.error(request, "User are not found")
            return redirect("/signin/")
        elif(user_data and user_data.Email_id != email):
            messages.error(request, "Email are not correct")
            return redirect("/signin/")
        
        elif(user_data and not check_password(password, user_data.Password)):
            messages.error(request, "Password are not correct")
            return redirect("/signin/")
        elif(user_data):
            request.session["username"] = username
            request.session["authenticated"] = True
            request.session["role"] = role
            return redirect("/")
    return render(request, "login.html")

def signup(request):
    if(request.method == 'POST'):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        picture = request.FILES.get("picture")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        conform_password = request.POST.get("conform_password")
        line = request.POST.get("line")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        role = request.POST.get("role")

        check_user = Users.objects.filter(Username = username, Role = role).first()

        if(check_user):
            messages.error(request, "User alrady exists")
            return redirect('/signup')
        elif(not check_user and password != conform_password):
            messages.error(request, "Password and Repassword are not same")
            return redirect('/signup')
        else:
            if(picture):
                picture_name = default_storage.save(f"static/images/{picture}", picture)
                picture_url = default_storage.url(picture_name)
            else:
                picture_url = None
            user_data= Users(First_Name = first_name, Last_Name = last_name, Profile_Picture = picture_url, Username = username, Email_id = email, Role = role, Password = make_password(password))
            user_data.save()

            userAddress_data = Address(	Username_id	= user_data.id, Line = line, city = city, state = state, pincode = pincode)
            userAddress_data.save()

            messages.success(request, "Sucessfully saved")
            return redirect('/signin')
    return render(request, "signup.html")


def logout(request):
    print("Hello")
    if("authenticated" in request.session.keys() and request.session["authenticated"]):
        request.session.clear()
        messages.success(request, "Sucessfully logout")
    return redirect("/signin/")
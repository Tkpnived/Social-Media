from itertools import chain
from operator import attrgetter

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from socialapp.models import logindb, Message,updb, follows,like,postm,Status

# Create your views here.

def home(request):
    return render(request,"home.html")
def reg(request):
    return render(request,"reg.html")


def register(request):
    alert=False
    if request.method == "POST":
        n = request.POST.get("name")
        e = request.POST.get("email")
        m = request.POST.get("mobile")
        pl = request.POST.get("place")
        g = request.POST.get("gender")
        p = request.POST.get("password")
        c = request.POST.get("password2")
        if "image" not in request.FILES:
            messages.error(request, "Please choose an image.")
            return redirect(reg)

        i = request.FILES["image"]
        if logindb.objects.filter(username=n).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
        elif logindb.objects.filter(email=e).exists():
            messages.error(request, "Email already exists. Please use a different email address.")
        elif p != c:
            messages.error(request, "Password and Confirm Password do not match.")
            return redirect(reg)
        else:
            obj = logindb(username=n, email=e, mobile=m,gender=g,place=pl, password=p, confirm_password=c,image=i)
            obj.save()
            messages.success(request, "Registration successful! Please log in.")
    return redirect(home)

def web(request):
    datas = updb.objects.all().order_by('-timestamp')
    alse = logindb.objects.all()
    alses = follows.objects.filter(username=request.session.get('name'))
    als = Status.objects.exclude(user=request.session.get('name')).all()

    user_object = None
    if request.session.get('name'):
        username = request.session['name']
        user_object = logindb.objects.get(username=username)
        log = logindb.objects.filter(username=username)
        alls= Status.objects.filter(user=username)
        logs = logindb.objects.all()
        following_users = follows.objects.filter(username=username).values_list('name', flat=True)
        data = follows.objects.filter(username=username)
        follow = follows.objects.filter(name=username)
        foll_users = follows.objects.filter(name=username)

    return render(request, "web.html", {"datas": datas,
                                        "user_object": user_object, "log": log,
                                        "als": als, "foll_usernames": foll_users, "following_users": following_users,
                                        "data": data, "follow": follow, "logs": logs, "alse": alse, "alses": alses,
                                        "alls": alls})

def loginusers(request):
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')

        if logindb.objects.filter(username=name_r, password=password_r).exists():
            user_object = logindb.objects.get(username=name_r)
            request.session['name'] = name_r
            request.session['password'] = password_r
            request.session['is_admin'] = False
            return redirect('web')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'home.html')


def logout(request):
    if 'password' in request.session:
        del request.session['password']
    if 'name' in request.session:
        del request.session['name']
    return redirect(home)

def search(request):
    query = request.GET.get('q')
    data = logindb.objects.filter(username__icontains=query)
    return render(request, 'search.html', {"data":data})

def profile(request,dataid,item):

    if 'name' in request.session:
        username = request.session['name']
        datas = follows.objects.filter(username=username)
        follow = follows.objects.filter(name=item)
        data = updb.objects.filter(username=dataid)
        user_object = None
        if request.session.get('name'):
            username = request.session['name']
            user_object = logindb.objects.get(username=username)

        return render(request, 'profile.html', {"data":data,"datas":datas,"follow":follow, "user_object": user_object})


def message(request, dataid):
    if 'name' in request.session:
        username = request.session['name']
        data = postm.objects.filter(username=username, name=dataid)
        datas = postm.objects.filter(name=username, username=dataid)
        msgs = logindb.objects.filter(username=dataid)
        datass = postm.objects.filter(username=dataid)

        all_msgs = sorted(
            chain(data, datas),
            key=attrgetter('timestamp'),
            reverse=True
        )

        unique_names = set(i.name for i in datass)

        return render(request, 'messages.html', {"msgs": msgs, "data": data, "datas": datas, "all_msgs": all_msgs, "unique_names": unique_names})


from django.contrib.auth.decorators import login_required

from django.utils import timezone

@login_required
def send_message(request, receiver_id):
    receiver = logindb.objects.get(pk=receiver_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            message = Message.objects.create(sender=request.user, receiver=receiver, content=content, timestamp=timezone.now())
            return redirect('message.html')  # You can customize this to redirect to the user's inbox

    return render(request, 'message.html', {'receiver': receiver})

def person(request, dataid, item):
    if 'name' in request.session:
        username = request.session['name']

        # Retrieve user details
        per = logindb.objects.filter(username=dataid)
        datas = updb.objects.filter(username=item)

        # Check if the logged-in user is following the specified user
        is_following = follows.objects.filter(username=username, name=item).exists()

        # Retrieve the logged-in user's followings
        data = follows.objects.filter(username=username)

        # Retrieve followings of the specified user
        followings = follows.objects.filter(username=item)

        return render(request, "person.html", {"per": per, "data": data, "datas": datas, "followings": followings, "is_following": is_following})



def updbs(request,dataid,item):
    alert = False

    if request.method == "POST":
        u = request.POST.get("username")
        i = request.FILES["image"]
        v = request.FILES.get("video")

        if u:
            obj = updb(username=u, image=i, video=v)
            obj.save()

            url = reverse('profile', kwargs={'dataid': dataid,"item":item})
            return redirect(url)

    return render(request, 'web.html', {'alert': alert})

def follow(request, dataid,item):
    alert = False

    if request.method == "POST":
        username = request.POST.get("username")
        follower = request.POST.get("follower")
        name = request.POST.get("name")

        is_following = follows.objects.filter(username=username, name=name, followers=follower).exists()
        if is_following:

            follows.objects.filter(username=username, name=name, followers=follower).delete()

        else:

            obj = follows(username=username, name=name, followers=follower)
            obj.save()
        url = reverse('person', kwargs={'dataid': dataid,'item': item})
        return redirect(url)

    return render(request, 'web.html', {'alert': alert})


def likess(request,dataids,items):
    alert = False

    if request.method == "POST":
        username = request.POST.get("username")
        likes = request.POST.get("likes")
        existing_like = like.objects.filter(username=username).first()

        if existing_like:
            # User has already liked, remove the like
            existing_like.delete()
        else:
            # User has not liked, add a new like
            obj = like(username=username, likes=likes)
            obj.save()
        url = reverse('web', kwargs={'dataids': dataids, 'items': items})
        return redirect(url)

    return render(request, 'web.html', {'alert': alert})


def postmessage(request, dataid):
    alert = False

    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        msg = request.POST.get("msg")

        # Use get method with a default value for 'image' to avoid MultiValueDictKeyError
        image = request.FILES.get("image", None)

        obj = postm(username=username, name=name, msg=msg, image=image)
        obj.save()

        url = reverse('message', kwargs={'dataid': dataid})
        return redirect(url)

    return render(request, 'web.html', {'alert': alert})

def edit(request,dataids):
    edits=logindb.objects.filter(username=dataids)
    user_object = None
    if request.session.get('name'):
        username = request.session['name']
        user_object = logindb.objects.get(username=username)
    return render(request,"edit.html",{'edits': edits,'user_object': user_object})


def update_image(request, dataid,item):
    if request.method == "POST":
        try:
            IM = request.FILES['image']
            FS = FileSystemStorage()
            file = FS.save(IM.name, IM)
            logindb.objects.filter(username=dataid).update(image=file)
        except MultiValueDictKeyError:
            messages.error(request, 'No image provided for update.')
    url = reverse('profile', kwargs={'dataid': dataid,'item': item})
    return redirect(url)

def update_profile(request, dataid,item):
    if request.method == "POST":
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        place = request.POST.get("place")
        logindb.objects.filter(username=dataid).update(place=place, email=email, mobile=mobile)
    url = reverse('profile', kwargs={'dataid': dataid, 'item': item})
    return redirect(url)

def status(request,dataid):
    sta=Status.objects.filter(user=dataid)
    return render(request,"status.html",{"sta":sta})

def addstatus(request):
    alert = False

    if request.method == "POST":
        u = request.POST.get("user")
        i = request.FILES["image"]

        obj =Status(user=u, image=i)
        obj.save()


    return redirect(web)
def foll(request,dataid,item):
    sta=follows.objects.filter(username=dataid)
    stase = logindb.objects.filter(username=item)
    return render(request,"follow.html",{"sta":sta,"stase":stase})

def followers(request,dataid,item):
    sta=follows.objects.filter(name=dataid)
    stase = logindb.objects.filter(username=item)
    return render(request,"followers.html",{"sta":sta,"stase":stase})

def mes(request,dataid):
    datas = postm.objects.filter(username=dataid)
    unique_names = set(i.name for i in datas)
    return render(request,"mes.html",{"datas": datas, "unique_names": unique_names})


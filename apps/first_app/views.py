from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "first_app/home.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.user_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='registration_errors')
            return redirect('/')
        else: 
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password_hash)
            user = User.objects.get(email=request.POST['email'])
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email
            request.session['id'] = user.id
            print ("==========successfully registered========")
            return redirect('/home')    

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if not len(user):
        errors = User.objects.login_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login_errors')
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
        user_login = User.objects.get(email=request.POST['email'])
        request.session['first_name'] = user_login.first_name
        request.session['last_name'] = user_login.last_name
        request.session['email'] = user_login.email
        request.session['id'] = user_login.id
        return redirect('/home')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect("/")

def home(request):    
    if "id" not in request.session:
        return redirect("/")
    else:
        quotes = Quote.objects.all()
        user = User.objects.get(id=request.session['id'])
        context = {
            'quotes': quotes,
            'user': user,
        }
        return render(request, 'first_app/quotes_home.html', context)

def add_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='quote_errors')
            return redirect('/home')
        else: 
            user = User.objects.get(email=request.session['email'])
            Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'], posted_by=user)
            return redirect('/home')

def edit_account(request):
    if request.method == 'POST':
        errors = User.objects.edit_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='edit_errors')
            return redirect('/show_edit_account')
        else:
            user = User.objects.get(id=request.session['id'])
            user.first_name=request.POST['first_name']
            user.last_name=request.POST['last_name']
            user.email=request.POST['email']
            user.save()
            return redirect("/home")        
    return redirect("/show_edit_account")

def show_edit_account(request):
    return render(request, 'first_app/edit_account.html')

def show_user(request, id):
    if "email" not in request.session: 
        return redirect("/")
    else: 
        context = {
            'user': User.objects.get(id=id),
            'quote': Quote.objects.filter(posted_by=User.objects.get(id=id))
        }
        return render(request, 'first_app/user_quotes.html', context)

def destroy(request,id):
    quote_to_delete = Quote.objects.get(id=id)
    quote_to_delete.delete()
    return redirect('/home')


def create_like(request, id):
    message = Quote.objects.get(id=id)
    print(message.author)
    user = User.objects.get(id=request.session['id'])
    if Like.objects.filter(liked_message=message, liker=user):
        messages.error(request,"You can't like a quote more than once!",extra_tags=message.quote)
        return redirect('/home')
    else:
        new_like = Like.objects.create(liked_message=message,liker=user)
        new_like.save()
        return redirect('/home')







        








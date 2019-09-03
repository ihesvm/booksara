import string
from json import JSONEncoder
from datetime import datetime
from random import random

from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

from .models import New, Book, Passwordresetcode, Token

random_str = lambda N: ''.join(
    random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# login , (API) , returns : JSON = status (ok|error) and token


@csrf_exempt
def news(request):
    news = New.objects.all().order_by('-date')[:11]
    news_serialized = serializers.serialize("json", news)
    return JsonResponse(news_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def login(request):
    # check if POST objects has username and password
    if 'username' in request.POST.keys() and 'password' in request.POST.keys():
        username = request.POST['username']
        password = request.POST['password']
        this_user = get_object_or_404(User, username=username)
        if (check_password(password, this_user.password)):  # authentication
            this_token = get_object_or_404(Token, user=this_user)
            token = this_token.token
            context = {}
            context['result'] = 'ok'
            context['token'] = token
            # return {'status':'ok','token':'TOKEN'}
            return JsonResponse(context, encoder=JSONEncoder)
        else:
            context = {}
            context['result'] = 'error'
            # return {'status':'error'}
            return JsonResponse(context, encoder=JSONEncoder)


# register (web)


def register(request):
    if 'requestcode' in request.POST.keys():  # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        # is this spam? check reCaptcha
        # duplicate email
        if User.objects.filter(email=request.POST['email']).exists():
            context = {
                'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)
        # if user does not exists
        if not User.objects.filter(username=request.POST['username']).exists():
            code = get_random_string(length=32)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = Passwordresetcode(
                email=email, time=now, code=code, username=username, password=password)
            temporarycode.save()
            message = 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'
            message = 'قدیم ها ایمیل فعال سازی می فرستادیم ولی الان شرکتش ما رو تحریم کرده (: پس راحت و بی دردسر'
            body = " برای فعال کردن اکانت بوکسرا خود روی لینک روبرو کلیک کنید: <a href=\"{}?code={}\">لینک رو به رو</a> ".format(
                request.build_absolute_uri('/accounts/register/'), code)
            message = message + body
            context = {
                'message': message}
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)
    elif 'code' in request.GET.keys():  # user clicked on code
        code = request.GET['code']
        if Passwordresetcode.objects.filter(
            code=code).exists():  # if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcode.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password,
                                          email=new_temp_user.email)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)
            # delete the temporary activation code from db
            Passwordresetcode.objects.filter(code=code).delete()
            context = {
                'message': 'اکانت شما ساخته شد. توکن شما {} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی!'.format(
                    this_token)}
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'register.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)


# return username based on sent POST Token


@csrf_exempt
@require_POST
def whoami(request):
    if 'token' in request.POST.keys():
        this_token = request.POST['token']  # TODO: Check if there is no `token`- done-please Check it
        # Check if there is a user with this token; will return 404 instead.
        this_user = get_object_or_404(User, token__token=this_token)

        return JsonResponse({
            'user': this_user.username,
        }, encoder=JSONEncoder)  # return {'user':'USERNAME'}

    else:
        return JsonResponse({
            'message': 'لطفا token را نیز ارسال کنید .',
        }, encoder=JSONEncoder)  #



@csrf_exempt
@require_POST
def query_book(request):
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    book = Book.objects.filter(publisher=this_user)
    book_serialized = serializers.serialize("json", book)
    return JsonResponse(book_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def generalstat(request):
    # TODO: should get a valid duration (from - to), if not, use 1 month
    # TODO: is the token valid?
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    books = Book.objects.filter(publisher=this_user).aggregate(
        Count('price'), Sum('price'))
    book = Book.objects.filter(publisher=this_user).aggregate(
        Count('price'), Sum('price'))
    context = {'sold': book, 'byed': books}
    # return {'income':'INCOME','expanse':'EXPANSE'}
    return JsonResponse(context, encoder=JSONEncoder)


# homepage of System


def index(request):
    context = {}
    return render(request, 'index.html', context)


@csrf_exempt
@require_POST
def edit_book(request):
    """edit an income"""
    this_name = request.POST['name'] if 'name' in request.POST else ""
    this_price = request.POST['price'] if 'price' in request.POST else "0"
    this_description = request.POST['description'] if 'description' in request.POST else ""
    this_sold = request.POST['is_sold'] if 'is_sold' in request.POST else False
    this_picture = request.POST['picture'] if 'picture' in request.POST else None
    this_date = request.POST['date'] if 'date' in request.POST else datetime.now()
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_publisher = get_object_or_404(User, token__token=this_token)
    this_pk = request.POST['id'] if 'id' in request.POST else "-1"

    this_book = get_object_or_404(Book, pk=this_pk, publisher=this_publisher)
    this_book.name = this_name
    this_book.price = this_price
    this_book.description = this_description
    this_book.is_sold = this_sold
    this_book.picture = this_picture
    this_book.date = this_date

    this_book.save()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


@csrf_exempt
@require_POST
def submit_book(request):
    """ submit an income """

    # TODO: revise validation for the amount
    this_name = request.POST['name'] if 'name' in request.POST else ""
    this_description = request.POST['description'] if 'description' in request.POST else ""
    this_picture = request.POST['picture'] if 'picture' in request.POST else None
    this_sold = request.POST['is_sold'] if 'is_sold' in request.POST else False
    this_price = request.POST['price'] if 'price' in request.POST else "-1"
    this_date = request.POST['date'] if 'date' in request.POST else timezone.now()
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_publisher = get_object_or_404(User, token__token=this_token)

    Book.objects.create(name=this_name, description=this_description, picture=this_picture, is_sold=this_sold,
                        price=this_price, date=this_date, publisher=this_publisher)
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


@csrf_exempt
def logout_url(request):
    # if not request.user.is_anonymous():
    logout(request)
    return redirect('/')

from email import message
import requests
import time
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from todo_list.models import T_List , crypto_tbl
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout as logouts
import json 
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Contact

api_key = "ab46b74033c243b48a3e7dbeaf889c0c"
tickers = ["MSFT","AAPL","TSLA", "AAT", "AMZN", "GOOGL","META", "JPM"]
crypto_tickers = ["BTC/USD", "ETH/USD", "AAC/USD","ACAT/USD", "ADA/USD", "BNB/USD", "XRP/USD", "XLM/USD"]
def home(request):
    if request.session.has_key('aut') == 1:
        apidata = []
        for x in crypto_tickers:
            stockdata = get_stock_quote(x, api_key)
            apidata.append(stockdata)
            
        return render(request, 'home.html', {'apidata':apidata})
    else:
        return redirect('authlogin')
def logout(request):
    logouts(request)
    return redirect('home')


def get_stock_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    # price = response['price']
    return response

def get_stock_quote(ticker_symbol, api):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    return response

def get_values(stockdata):
    
    exchange = stockdata['exchange'],
    currency = stockdata['currency'],
    open_price = stockdata['open'],
    high_price = stockdata['high'],
    low_price = stockdata['low'],
    close_price = stockdata['close'],
    volume = stockdata['volume']
    list = {'Exchange' : exchange, 'currency' : currency, 'open_price' : open_price , 'high_price' : high_price, 'low_price':low_price , 'close_price' :close_price , 'volume' : volume }
    return list

def stockmarket(request):
    apidata = []
    for x in tickers:
        stockdata = get_stock_quote(x, api_key)
        apidata.append(stockdata)
    return render(request, 'stockmarket.html', {'apidata':apidata})

def marketnews(request):
    url ="https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=a1c9f226024b4892b6a941332ef6f33d"
    apidata = requests.get(url).json()
    articles = apidata["articles"]
    return render(request, 'marketnews.html', {'article':articles}, )

 

def cryptocurrency(request):
    apidata = []
    for x in crypto_tickers:
        cryptodata = get_stock_quote(x, api_key)
        apidata.append(cryptodata)
    return render(request, 'cryptocurrency.html', {'apidata':apidata})


def mailinbox(request) :
    return render(request, 'mailinbox.html', {})

def authlogin(request) :

    if request.method == "POST" :
        uname = request.POST['uname']
        pass1 = request.POST['pass']

        user = authenticate(username = uname, password = pass1)
        if user is not None: 
            login(request, user)
            fname = user.first_name
            u_id = user.id
            t_get = T_List.objects.all()
            for trans in t_get:
                if trans.u_id == u_id :
                    request.session['aut'] = 1
                    request.session['u_id'] = u_id
                    request.session['fname'] = user.first_name
                    request.session['email'] = user.email
                    request.session['token'] = trans.t_amt
            #eturn render(request, home, {'fname': fname})
            return redirect('home')

        else :
            messages.error(request,"Incorrect Credentials")
            return redirect('authlogin')

    return render(request, 'authlogin.html', {})

def authregister(request) :
    if request.method == "POST" :
        uname = request.POST['uname']
        pass1 = request.POST['pass']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']

        myuser = User.objects.create_user( uname, email , pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        ins = T_List(t_amt=5000,u_id=myuser.id)
        ins.save() 
        messages.success(request, "Registration successful")
        return redirect('authlogin')
    return render(request, 'authregister.html', {})


class ContactView(CreateView):
	model = Contact
	fields = '__all__'
	template_name = 'contact.html'
	success_url = reverse_lazy('home')

from email import message
import random
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
data=[]
arr = []
price_key= "c7f74c2b5893401f98da70a76b8d6b3f"
api_key3 = "47485a5e3a27424db697ceda50a89ad5"
api_key = "7044e59787c441439643122b1f87b498"
api_key1 = "cc5f05fc152a4ae5be1599009443440b"
api_key2 = "6b582ad68d184d709f0243dcceac5f47"
tickers = ["MSFT","AAPL","TSLA", "AAT", "AMZN", "GOOGL","META","IBM","TCS", "MDB","KALA","WW","SHOP","ACN","ADBE","NFLX"]

crypto_tickers = ["BTC/USD", "ETH/USD", "AAC/USD","ACAT/USD", "ADA/USD", "BNB/USD", "XRP/USD", "XLM/USD"]
def home(request):
    if request.session.has_key('aut') == 1:
        apidata = []
        for x in crypto_tickers:
            stockdata = get_stock_quote(x, api_key1)
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
    for x in range(0,7):
        stockdata = get_stock_quote(tickers[x], api_key)
        apidata.append(stockdata)
    
    for x in range(7,16):
        stockdata = get_stock_quote(tickers[x], api_key3)
        apidata.append(stockdata)
    
    

    return render(request, 'stockmarket.html', {'apidata':apidata})

def marketnews(request):
    url ="https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=a1c9f226024b4892b6a941332ef6f33d"
    apidata = requests.get(url).json()
    random.shuffle(apidata["articles"])
    articles = (apidata["articles"])
    return render(request, 'marketnews.html', {'article':articles}, )


def cryptocurrency(request):
    apidata = []
    for x in crypto_tickers:
        cryptodata = get_stock_quote(x, api_key2)
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

from django.shortcuts import render, redirect
from .models import Stock
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def portfolio(request):
    
    apidata = []
    for x in range(0,7):
        stockdata = get_stock_quote(tickers[x], api_key)
        apidata.append(stockdata)
    
    for x in range(7,16):
        stockdata = get_stock_quote(tickers[x], api_key3)
        apidata.append(stockdata)

     
    stock_name = ""
    if request.method == 'POST':
        stock_name = request.POST['stock_name']
        buying_price = request.POST['buying_price']
        quantity = request.POST['Quantity']
        user = request.user
        stock = Stock(name=stock_name, buying_price=buying_price, Quantity= quantity, user=user)
        stock.save()
        
        messages.success(request, 'Stock added successfully!')

    data = Stock.objects.all()
    
    for i in data:
        response = get_stock_price(i.name, price_key)
        price = response['price']
        arr.append(price)
        mylist = zip(data , arr)
    if not data:
        return redirect(add)
    return render(request,'portfolio.html',{'liste':mylist})

def delete_stock(request):
   
   stock_name = request.POST['name']
   current_price = request.POST['cur_price']
   index = 0
   for i in data:
      if i.name == stock_name :
        index = data.index(i) 
        break 
   arr.pop(index)
   Stock.objects.filter(name=stock_name).delete()
   
   return redirect(portfolio)


def add(request):
    apidata = []
    for x in range(0,7):
        stockdata = get_stock_quote(tickers[x], api_key)
        apidata.append(stockdata)
    
    for x in range(7,16):
        stockdata = get_stock_quote(tickers[x], api_key3)
        apidata.append(stockdata)

        
    return render(request,'add_stock.html', {'apidata':apidata})
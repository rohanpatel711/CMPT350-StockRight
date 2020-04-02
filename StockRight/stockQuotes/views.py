from .models import Stock
from .forms import StockForm, MyRegistrationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# IEX Publishable API Token: pk_8ffc6e63445e477fa4c225e7f9a30694 
# WTD Token (For Indices): lFxr8LrnAm6SsyOVrYZ7Z7Q4G4TOCAeGx6ikjFCCexwcbu8J6zuCOvUys69A
# Company name to ticker
# http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=dollarama&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback

def register(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)

            subject = "Welcome to StockRight, "+str(username)+"!"
            message = "We hope our simplistic UI helps you manage your portfolio with zero clutter.\nThank you for your business.\n\nHappy Investing!\nStockRight Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject,message,from_email,to_list)

            messages.success(request, f'Email Sent! New Account Created: {username}')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f'Please try again.')
    else:
        form = MyRegistrationForm()
    return render(request, 'register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            messages.success(request, f'Welcome back {user.username}!')
            return redirect('home')
        else:
            messages.error(request, f'Please try again')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def obtainLogo(ticker):
    import requests
    import json

    url = "https://cloud.iexapis.com/stable/stock/"+ticker+"/logo?token=pk_8ffc6e63445e477fa4c225e7f9a30694"
    logo_req = requests.get(url)

    try:
        logo_url = json.loads(logo_req._content)
    except Exception as e:
        logo_url = "Invalid Ticker"

    return logo_url

def obtainCompanyData(ticker):
    import requests
    import json

    url = "https://cloud.iexapis.com/stable/stock/"+ticker+"/company?token=pk_8ffc6e63445e477fa4c225e7f9a30694"
    cInfo_req = requests.get(url)

    try:
        cInfo_url = json.loads(cInfo_req._content)
    except Exception as e:
        cInfo_url = "Company Info Unavailable"

    return cInfo_url

def getTickerFromName(company):
    import requests
    import json
    url1 = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+company+"&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
    company_req = requests.get(url1)

    try:
        company_data_string = company_req._content.decode()
        json_data_start_index = company_data_string.find('"Result":[{')+9
        company_data = json.loads(company_req._content.decode()[json_data_start_index:-4])
        cTicker = company_data[0]['symbol']
    except Exception as e:
        cTicker = "Invalid Company name."
    
    return cTicker

def stockSearch(ticker,company):
    import requests
    import json
    if company == "":
        url = "https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_8ffc6e63445e477fa4c225e7f9a30694"
        api_req = requests.get(url)

        try:
            api = json.loads(api_req._content)
            logo = obtainLogo(ticker)
            
            api['customLogo'] = logo['url']
            ytdChg = api['ytdChange']
            api['ytdChange'] = float(round(ytdChg*100,2))
            mktCap = api['marketCap']
            api['marketCap'] = str("{:,}".format(mktCap))
            avgVol = api["avgTotalVolume"]
            api["avgTotalVolume"] = str("{:,}".format(avgVol))

        except Exception as e:
            api = "Invalid Ticker"

        return api

    elif ticker == "":
        companyTicker = getTickerFromName(company)
        url2 = "https://cloud.iexapis.com/stable/stock/"+companyTicker+"/quote?token=pk_8ffc6e63445e477fa4c225e7f9a30694"
        api_req = requests.get(url2)
        try:
            api = json.loads(api_req._content)
            logo = obtainLogo(companyTicker)
            api['customLogo'] = logo['url']

            ytdChg = api['ytdChange']
            api['ytdChange'] = float(round(ytdChg*100,2))

            mktCap = api['marketCap']
            api['marketCap'] = str("{:,}".format(mktCap))

            avgVol = api["avgTotalVolume"]
            api["avgTotalVolume"] = str("{:,}".format(avgVol))

        except Exception as e:
            api = "Invalid Ticker"
            
        return api

def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST['ticker']
        company = request.POST['company']
        api = stockSearch(ticker,company)

        if ticker == "":
            cInfo = obtainCompanyData(getTickerFromName(company))
            if cInfo != "Company Info Unavailable":
                ceoName = cInfo['CEO']
                cInfo['customCEO'] = ceoName.replace(" ","_")
                no_of_employees = cInfo['employees']
                cInfo['employees'] = str("{:,}".format(no_of_employees))
            else:
                messages.error(request, f'{cInfo}')
        elif company == "":
            cInfo = obtainCompanyData(ticker)
            if cInfo != "Company Info Unavailable":
                ceoName = cInfo['CEO']
                cInfo['customCEO'] = ceoName.replace(" ","_")
                no_of_employees = cInfo['employees']
                cInfo['employees'] = str("{:,}".format(no_of_employees))
            else:
                messages.error(request, f'{cInfo}')
        
        if api == "Invalid Ticker":
            messages.error(request, f'{api}')
        elif api == "Invalid Company name.":
            messages.error(request, f'{api}')


        return render(request, 'home.html', {'api':api,'cInfo':cInfo})
    else:
        return render(request, 'home.html')

@login_required
def myStocks(request):
    import requests
    import json
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            sForm = form.save(user = request.user)
            sForm.user = request.user
            sForm.save()
            messages.success(request, f'{str(sForm.ticker).upper()} has been added to your Portfolio.')
            return redirect('myStocks')
    else:
        form = StockForm()
        CurrUser = request.user
        tickers = Stock.objects.filter(user=CurrUser)
        stock_data = []
    
        for ticker in tickers:
            url = "https://cloud.iexapis.com/stable/stock/"+str(ticker.ticker)+"/quote?token=pk_8ffc6e63445e477fa4c225e7f9a30694"
            api_req = requests.get(url)

            try:
                api = json.loads(api_req._content)
                stock_data.append(api)

            except Exception as e:
                api = "Invalid Ticker"
            
            idx = stock_data.index(api)
            stock_data[idx]['customQuantity'] = ticker.quantity
            stock_data[idx]['customBuyPrice'] = float(round(ticker.buyPrice,2))
            stock_data[idx]['customTotalValue'] = ticker.quantity*stock_data[idx]['latestPrice']
            stock_data[idx]['customTotalReturn'] = float(round(((stock_data[idx]['customTotalValue'])-float(ticker.quantity*ticker.buyPrice)),2))
            difference = stock_data[idx]['customTotalValue'] - float(ticker.quantity*ticker.buyPrice)
            originalPrice = float(ticker.quantity*ticker.buyPrice)
            stock_data[idx]['customTotalReturnPercent'] = float(round((difference/originalPrice)*100,2))
            stock_data[idx]['customPurchaseDate'] = str(ticker.added_at)
            stock_data[idx]['customStock_id'] = ticker.id


        return render(request, 'myStocks.html', {'form':form,'ticker':tickers,'user':CurrUser, 'stock_data':stock_data})

@login_required
def deleteStock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, f'{str(item.ticker).upper()} has been deleted from your Portfolio.')
    return redirect('myStocks')
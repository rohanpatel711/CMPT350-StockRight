from django.shortcuts import render

# IEX API key: pk_6e6c4c5ea9f843ca94619cf3957d691a

# Homepage view function
# Request = browser request
# Return and render a new page (in this case the home page)
def home(request):
    # Used for API
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST['ticker']
        url = "https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_8ffc6e63445e477fa4c225e7f9a30694"
        api_req = requests.get(url)

        try:
            api = json.loads(api_req._content)
        except Exception as e:
            api = "Error"
        return render(request, 'home.html', {'api':api})
    else:
        return render(request, 'home.html', {'ticker':'Enter Ticker Symbol above.'})


# About Me page view function
def about(request):
    return render(request, 'about.html', {})


def myStocks(request):
    return render(request, 'myStocks.html', {})


def index(request):
    import requests
    import json
    url = "https://stocknewsapi.com/api/v1/category?section=general&items=50&token=ubtrdde1nxakqqfeasdp1urmiz7xgxi4a1aqo25n"
    url1 = "https://stocknewsapi.com/api/v1/top-mention?&date=last30days&token=fyrd2wiyzfxnbvm69itcoq2bzszuywolnfxcetqx"
    api_req = requests.get(url)
    api_req1 = requests.get(url1)
    try:
        data = json.loads(api_req._content)
        data1 = json.loads(api_req1._content)
    except Exception as e:
        api = "Error"
    return render(request, 'index.html', {'api': data, 'api1':data1})

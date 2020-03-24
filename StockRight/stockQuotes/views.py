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
        url = "https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_6e6c4c5ea9f843ca94619cf3957d691a"
        api_req = requests.get(url)

        try:
            api = json.loads(api_req._content)
        except Exception as e:
            api = "Error"
        return render(request, 'home.html', {'api':api})
    else:
        return render(request, 'home.html', {'ticker':'Enter Ticker above.'})


# About Me page view function
def about(request):
    return render(request, 'about.html', {})

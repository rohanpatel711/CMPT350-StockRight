from django.shortcuts import render

# Create your views here.
def news(request):
    # Used for API
    import requests
    import json
    url = "https://stocknewsapi.com/api/v1/category?section=alltickers&items=50&token=ubtrdde1nxakqqfeasdp1urmiz7xgxi4a1aqo25n"
    api_req = requests.get(url)
    try:
        data = json.loads(api_req._content)
    except Exception as e:
        api = "Error"
    return render(request, 'news.html', {'api': data})

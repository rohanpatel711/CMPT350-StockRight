from django.shortcuts import render

# Homepage view function
# Request = browser request
# Return and render a new page (in this case the home page)
def home(request):
    return render(request, 'home.html', {})

# About Me page view function
def about(request):
    return render(request, 'about.html', {})
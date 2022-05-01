from django.shortcuts import render


def home(request):
    import requests
    import json

    if request.method == "POST":
        initial_date = request.POST['initial_date']
        final_date = request.POST['final_date']

        api_request = requests.get("https://api.vatcomply.com/rates?date=" + str(initial_date))

        try:
            api = json.loads(api_request.content)
        except Exception as e:  # todo fix exception clause
            api = "Error.."

        return render(request, 'home.html', {'api': api})

    else:

        return render(request, 'home.html', {})

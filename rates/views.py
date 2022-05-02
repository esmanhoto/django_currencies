from django.shortcuts import render, redirect
from .models import Rate
from django.contrib import messages
from rest_framework import viewsets
from .serializers import RateSerializer


class RateView(viewsets.ModelViewSet):
    queryset = Rate.objects.all().order_by('date')
    serializer_class = RateSerializer


def home(request):
    import requests
    import json
    from datetime import date
    from datetime import timedelta

    date_list = []
    today = date.today()

    while len(date_list) < 6:
        if today.isoweekday() < 6:
            date_list.append(today)
        today -= timedelta(days=1)

    if request.method == "POST":
        initial_date = request.POST['initial_date']
        final_date = request.POST['final_date']

        date_list = []
        date1 = date.fromisoformat(initial_date)
        date2 = date.fromisoformat(final_date)

        if date2 < date1:
            messages.success(request, "Please, choose an initial date earlier than the final date!")
            return redirect(home)

        else:

            if date1.isoweekday() < 6:
                date_list.append(date1)
            while date2 != date1:
                date1 += timedelta(days=1)
                if date1.isoweekday() < 6:
                    date_list.append(date1)

            if len(date_list) > 5:
                messages.success(request, "Maximum period of time is 5 weekdays. Please, choose a smaller interval!")
                return redirect(home)

            else:

                for day in date_list:
                    api_request = requests.get("https://api.vatcomply.com/rates?date=" + str(day))

                    try:
                        api = json.loads(api_request.content)
                    except Exception as e:  # todo fix exception clause
                        api = "Error.."

                    euro = round(api['rates']['EUR'] / api['rates']['USD'], 4)
                    real = round(api['rates']['BRL'] / api['rates']['USD'], 4)
                    yen = round(api['rates']['JPY'] / api['rates']['USD'], 4)

                    rate_data = Rate.objects.get_or_create(date=day, euro=euro, real=real, yen=yen)

        all_rates = Rate.objects.all().order_by('date')

        return render(request, 'home.html', {'all_rates': all_rates, 'date_list': date_list})

    else:
        all_rates = Rate.objects.all().order_by('date')
        return render(request, 'home.html',
                      {'all_rates': all_rates, 'date_list': date_list})

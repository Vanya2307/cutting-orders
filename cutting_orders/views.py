
from django.shortcuts import render



def home(request):

    context = {}

    if request.user.is_authenticated:
        orders = request.user.orders

        context['drafts_count'] = orders.filter(
            status='DRAFT',
        ).count

        context['submitted_count'] = orders.filter(
                    status='SUBMITTED',
                ).count


    return render(request, "home.html", context)
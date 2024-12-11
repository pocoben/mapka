# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import *
from django.db.models import Count, Q
import random
from django.db import IntegrityError
from django.contrib.auth.models import User  # Import User model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Avg


def home_view(request):
    if request.user.is_authenticated:
        woj = request.user.userinfo.wojewodztwo
        clickCount = request.user.userinfo.clickCount
        return render(
            request, "mapka/home.html", {"wojewodztwo": woj, "clickCount": clickCount}
        )
    return render(request, "mapka/home.html")


# Registration view
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            woj = form.cleaned_data["wojewodztwo"]
            UserInfo.objects.create(user=user, wojewodztwo=woj)
            login(request, user)
            return redirect("home_view")
    else:
        form = RegisterForm()
    return render(request, "mapka/register.html", {"form": form})


# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home_view")
    else:
        form = AuthenticationForm()
    return render(request, "mapka/login.html", {"form": form})


def edit_view(request):
    user_info, created = UserInfo.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        user_info_form = EditUserInfoForm(request.POST, instance=user_info)
        if user_form.is_valid() and user_info_form.is_valid():
            user_form.save()
            user_info_form.save()
            return redirect("edit_view")
    else:
        user_form = EditUserForm(instance=request.user)
        user_info_form = EditUserInfoForm(instance=user_info)
    return render(
        request,
        "mapka/edit.html",
        {"user_form": user_form, "user_info_form": user_info_form},
    )


# def wykres(request):
#     # Aggregate user counts by województwo
#     wojewodztwa_counts = (
#         UserInfo.objects.values('wojewodztwo')
#         .annotate(count=Count('user'))
#         .order_by('wojewodztwo')
#     )

#     print(wojewodztwa_counts)

#     # Prepare the data for the heatmap
#     labels = []
#     data = []

#     for entry in wojewodztwa_counts:
#         labels.append(entry['wojewodztwo'])
#         data.append(entry['count'])

#     return render(request, 'mapka/map.html', {'labels' : labels, 'data' : data})


def map_view(request):
    # Aggregate counts of users per province code
    wojewodztwa_counts = UserInfo.objects.values("wojewodztwo").annotate(
        count=Count("wojewodztwo")
    )

    plec_counts = UserInfo.objects.values("wojewodztwo").annotate(
        male_count=Count("id", filter=Q(plec="m")),
        female_count=Count("id", filter=Q(plec="k")),
    )

    click_counts = UserInfo.objects.values(
        "wojewodztwo"
    ).annotate(  # Group by wojewodztwo
        total_clicks=Sum("clickCount")
    )  # Sum clickCount for each wojewodztwo

    age_counts = UserInfo.objects.values(
        "wojewodztwo"
    ).annotate(  # Group by wojewodztwo
        average_ages=Avg("wiek")
    )

    # Convert the query result to a dictionary like {"PL-ZP": 50, ...}
    wojewodztwa_counts = {
        item["wojewodztwo"]: item["count"] for item in wojewodztwa_counts
    }

    male_counts = {entry["wojewodztwo"]: entry["male_count"] for entry in plec_counts}
    female_counts = {
        entry["wojewodztwo"]: entry["female_count"] for entry in plec_counts
    }

    click_counts = {item["wojewodztwo"]: item["total_clicks"] for item in click_counts}

    age_counts = {item["wojewodztwo"]: item["average_ages"] for item in age_counts}

    # Render the map template with wojewodztwa_counts in the context
    return render(
        request,
        "mapka/map.html",
        {
            "wojewodztwa_counts": wojewodztwa_counts,
            "male_counts": male_counts,
            "female_counts": female_counts,
            "click_counts": click_counts,
            "age_counts": age_counts,
        },
    )


def generate_random_users(num_users=100):
    # Prepare usernames and wojewodztwa for bulk creation
    usernames = [f"user{i}" for i in range(1, num_users + 1)]
    wojewodztwa = [choice[0] for choice in UserInfo.WOJEWODZTWO_CHOICES]
    plec = [choice[0] for choice in UserInfo.PLEC_CHOICES]

    # Step 1: Bulk create User objects
    users = [
        User(username=username, password="defaultpassword") for username in usernames
    ]
    User.objects.bulk_create(users, ignore_conflicts=True)

    # Step 2: Retrieve the newly created User objects (assuming all have unique usernames)
    saved_users = User.objects.filter(username__in=usernames)

    # Step 3: Bulk create UserInfo objects with saved User instances
    user_infos = [
        UserInfo(
            user=user,
            wojewodztwo=random.choice(wojewodztwa),
            plec=random.choice(plec),
            clickCount=random.randrange(1, 100),
            wiek=random.randrange(10, 100),
        )
        for user in saved_users
    ]
    UserInfo.objects.bulk_create(user_infos)

    return [user.username for user in saved_users]


def generate_users_view(request):

    users_created = generate_random_users()

    return render(
        request,
        "mapka/generate_users.html",
        {
            "users_created": users_created,
        },
    )


def remove_users_view(request):
    # Generate the usernames to delete (user1 to user100)
    usernames_to_delete = [f"user{i}" for i in range(1, 101)]

    # Filter users by those usernames
    users_to_delete = User.objects.filter(username__in=usernames_to_delete)

    # Delete the selected users
    deleted_count, _ = users_to_delete.delete()

    # Return a response with the number of deleted users
    return HttpResponse(f"Deleted {deleted_count} users.")


def chart_view(request):

    click_count = []
    wiek_count = []

    for i in UserInfo.objects.all():
        a = i.clickCount
        b = i.wiek
        click_count.append(a)
        wiek_count.append(b)

    return render(
        request,
        "mapka/chart.html",
        {"UserInfo": list(UserInfo.objects.values("wiek", "clickCount", "plec"))},
    )
    # return render(request, 'mapka/map.html', {'click_count' : click_count, 'wiek_count' : wiek_count})


@csrf_exempt
def click_count_view(request):
    userinfo = UserInfo.objects.get(user=request.user)
    userinfo.clickCount += 1
    userinfo.save()
    return JsonResponse({"clickCount": userinfo.clickCount})

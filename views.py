from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,"index.html")

from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        login(request, user)
        return redirect("appointment")

    return render(request, "registration.html")
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("appointment")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "1login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

# def index1(request):
#     return render(request,"index1.html")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Appointment

@login_required(login_url='login')
def my_bookings(request):
    bookings = Appointment.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment


@login_required(login_url='login')
def appointment(request):
    if request.method == 'POST':
        booking = Appointment.objects.create(
            user=request.user,
            name=request.user.first_name or request.user.username,
            doctor=request.POST.get('doctor'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            email=request.user.email,
            phone=request.POST.get('phone')
        )

        return redirect('receipt', appointment_id=booking.id)

    return render(request, 'index1.html')


@login_required(login_url='login')
def receipt(request, appointment_id):
    booking = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user
    )

    return render(request, 'receipt.html', {'booking': booking})

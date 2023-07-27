from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponse, HttpRequest
from .models import Player
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from .forms import PlayerForm, StatFilter, PlayerUpdateForm, CoachForm, PaymentForm, CoachUpdateForm
from django.http import JsonResponse
from .models import Events, Coach, Payment
import pandas as pd
# from plotly.offline import plot
# import plotly.express as px
from .utils import get_plot
from .utils import get_plot2
from .utils import get_plot3
from .utils import get_plot4
from .utils import get_plot5
from .utils import get_plot6
import base64
from PIL import Image
import io
###
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_data

# Create your views here.


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_data.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "You have successfully activated your account. You can log in to your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate user account"
    mail_message = render_to_string('activate_account.html',
                                    {
                                        'user': user.username,
                                        'domain': get_current_site(request).domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_data.make_token(user),
                                        'protocol': 'https' if request.is_secure() else 'http'
                                    }

                                    )
    email = EmailMessage(mail_subject, mail_message, to=[to_email])
    try:
        email.send()
    except:
        raise ValidationError(
            f"Problem sending confirmation email to {to_email}")
    else:
        messages.success(request, mark_safe(f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> and click on \
        the received activation link to confirm your registration. <br></br>  <b>Note:</b> Check your spam folder'))


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html', {'name': request.user})


def loginView(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.error(request, "Your account is not verified yet.")
                return redirect('login')
        except User.DoesNotExist:
            messages.error(
                request, "Incorrect username or password.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active == True:
            login(request, user)
            return redirect('home')
        elif user is not None and user.is_active == False:
            messages.error(
                request, "Your account is not verified yet.")

        else:
            messages.error(
                request, "Incorrect username or password.")

    return render(request, 'login.html')


def register_player(request):

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user.set_password(form.cleaned_data['password'])
            player.user.is_active = False
            player.save()
            activateEmail(request, player.user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            messages.error(request, "Error during registration")
    else:
        form = PlayerForm()

    context = {'form': form}
    return render(request, 'register-player.html', context)


def register_coach(request):

    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            coach = form.save(commit=False)
            coach.user.set_password(form.cleaned_data['password'])
            coach.user.is_active = False
            coach.save()
            activateEmail(request, coach.user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            messages.error(request, "Error during registration")
    else:
        form = CoachForm()

    context = {'form': form}
    return render(request, 'register-coach.html', context)


@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def playerstats(request):
    form = StatFilter(request.GET)
    if form.is_valid():
        stat = form.cleaned_data['stat']
        if stat == '':
            players = Player.objects.all().order_by('name')
        elif stat:
            players = Player.objects.all().order_by('-{}'.format(stat))
        else:
            players = Player.objects.all().order_by('name')
    else:
        players = Player.objects.all().order_by('name')
    return render(request, 'playerstats.html', {'form': form, 'players': players})


@login_required(login_url='login')
def addPlayer(request):
    form = PlayerForm()
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('playerstats')

    context = {'form': form}
    return render(request, 'addplayer.html', context)


@login_required(login_url='login')
def updatePlayer(request, pk):
    player = Player.objects.get(id=pk)
    form = PlayerUpdateForm(instance=player)

    if request.method == 'POST':
        form = PlayerUpdateForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('playerstats')

    context = {'form': form}
    return render(request, 'addplayer.html', context)


@login_required(login_url='login')
def deletePlayer(request, pk):
    player = Player.objects.get(id=pk)
    if request.method == 'POST':
        player.delete()
        return redirect('playerstats')
    context = {'player': player}
    return render(request, 'deleteplayer.html', context)


@login_required(login_url='login')
def playerProfile(request, pk):
    player = Player.objects.get(id=pk)
    context = {'player': player}
    return render(request, 'playerprofile.html', context)


##############################################################################################################
##############################################################################################################

def index(request):
    all_events = Events.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'index.html', context)


def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })

    return JsonResponse(out, safe=False)


@user_passes_test(lambda u: u.is_superuser)
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)


@user_passes_test(lambda u: u.is_superuser)
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


@user_passes_test(lambda u: u.is_superuser)
def remove(request, event_id):
    print("Event ID:", event_id)
    event = Events.objects.get(id=event_id)
    event.delete()
    data = {}
    return JsonResponse(data)


########################################################################################################
########################################################################################################
####################### VISUALS ####################################################
#################################################################################

def visuals(request):
    qs = Player.objects.all()
    names = [names.name for names in qs]
    fg = [fg.fieldgoals_percentage for fg in qs]
    chart1 = get_plot(names, fg, "Players Field Goal %",
                      "Players", "Field Goals Percentage")

    ppg = [ppg.points_per_game for ppg in qs]
    chart2 = get_plot2(names, ppg)

    apg = [apg.assists_per_game for apg in qs]
    chart3 = get_plot3(names, apg)

    tpp = [tpp.three_point_percentage for tpp in qs]
    chart4 = get_plot4(names, tpp)

    ftp = [ftp.free_throw_percentage for ftp in qs]
    chart5 = get_plot5(names, ftp)

    rpg = [rpg.rebounds_per_game for rpg in qs]
    chart6 = get_plot6(names, rpg)

    return render(request, 'graphindex.html', {'chart1': chart1, 'chart2': chart2, 'chart3': chart3, 'chart4': chart4, 'chart5': chart5, 'chart6': chart6})


################################################################################################################################################################################################################################################################################

def draw(request):
    return render(request, 'drawing.html')


def save_drawing(request):
    if request.method == 'POST':
        image_data = request.POST['image']
        # Decode the image data from base64
        decoded_image_data = base64.b64decode(image_data.split(',')[1])
        with open('drawing.png', 'wb') as f:
            f.write(decoded_image_data)
        return HttpResponse('Drawing saved successfully')
    else:
        return HttpResponse('Invalid request')


def view_drawing(request):
    with open('drawing.png', 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')


############################################## Payments ############################################
@user_passes_test(lambda u: u.is_superuser)
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return redirect('home')
        else:
            messages.error(request, "Error making payment")
    else:
        form = PaymentForm()

    context = {'form': form}
    return render(request, 'payments.html', context)


def displayPayments(request):
    payments = Payment.objects.all()
    return render(request, 'displaypayments.html', {'payments': payments})

############################ Coach CRUD ##############################


@login_required(login_url='login')
def displaycoaches(request):
    coaches = Coach.objects.all().order_by('name')
    return render(request, 'displaycoaches.html', {'coaches': coaches})


@login_required(login_url='login')
def updateCoach(request, pk):
    coach = Coach.objects.get(id=pk)
    form = CoachUpdateForm(instance=coach)

    if request.method == 'POST':
        form = CoachUpdateForm(request.POST, instance=coach)
        if form.is_valid():
            form.save()
            return redirect('displaycoaches')

    context = {'form': form}
    return render(request, 'update-coach.html', context)


@login_required(login_url='login')
def deleteCoach(request, pk):
    coach = Coach.objects.get(id=pk)
    if request.method == 'POST':
        coach.user.delete()
        coach.delete()
        return redirect('displaycoaches')
    context = {'coach': coach}
    return render(request, 'delete-coach.html', context)


@login_required(login_url='login')
def coachProfile(request, pk):
    coach = Coach.objects.get(id=pk)
    context = {'coach': coach}
    return render(request, 'coachprofile.html', context)

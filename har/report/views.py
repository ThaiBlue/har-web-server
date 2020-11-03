from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .forms import ReportForm
from .models import Report

# connection view
def render_connection_view(request):
    
    # user has already logged
    if request.user.is_authenticated:
        return redirect('reports')

    # handle connect request
    if request.method == 'POST': 
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            authenticate(request, username=email, password=password)
        except:
            user = None
        else:
            user = authenticate(request, username=email, password=password)

        # if user information is available
        if user is not None:
            # logging in
            login(request, user)
            return redirect('reports')

        # if user information is not available
        else:
            try: # try to create the user
                User.objects.create_user(username=email, email=email, password=password)
            except:
                messages.error(request, "Wrong password!!")
                return redirect('connection')

            else:# if user does not exist
                #create user        
                user = User.objects.create_user(username=email, email=email, password=password)
                #logging in
                login(request, user)
                return redirect('reports')

    return render(request, 'connection.html', {})

# report creation view
def render_report_creation_view(request):

    # if user has not logged yet
    if not request.user.is_authenticated:
        return redirect('connection')

    # handle report submission request
    if request.method == 'POST':

        # process request data
        if request.POST.get('accuracy') == '': # if accuracy are null
            data = {
                'user' : request.user,
                'name' : request.POST.get('name'),
                'latitude' : float(request.POST.get('latitude')),
                'longitude' : float(request.POST.get('longitude')),
                'altitude' : float(request.POST.get('altitude'))
            } 

        else:
            data = {
                'user' : request.user,
                'name' : request.POST.get('name'),
                'latitude' : float(request.POST.get('latitude')),
                'longitude' : float(request.POST.get('longitude')),
                'altitude' : float(request.POST.get('altitude')),
                'accuracy' : float(request.POST.get('accuracy'))
            }

        # generate a report form
        form = ReportForm(data)
        
        # validate form
        if form.is_valid():
            # insert information into database
            form.save()

            #redirect page
            return redirect('reports')

    return render(request, 'report_creation.html', {})

# update view
def render_report_update_view(request, id):

    # if user has not logged yet
    if not request.user.is_authenticated:
        return redirect('connection')
    
    # verify if report exists
    try:
        Report.objects.get(id=id)
    except:
        return HttpResponse(b'<h1>Not Found<h1>', status=404)
    
    # get report from database
    report = Report.objects.get(id=id)

    # verify the creator
    if request.user != report.user:
        return HttpResponse(b'<h1>Permission Denied<h1>', status=403)

    # process report data
    if report.accuracy is None:
        accuracy = ''
    else:
        accuracy = report.accuracy

    # handle POST request
    if request.method == 'POST':

        # update report information
        report.name = request.POST.get('name')
        report.latitude = request.POST.get('latitude')
        report.longitude = request.POST.get('longitude')
        report.altitude = request.POST.get('altitude')
        accuracy = accuracy

        # commit update information
        report.save()

        return redirect('reports')

    # create context
    context = {
        'name' : report.name,
        'latitude' : report.latitude,
        'longitude' : report.longitude,
        'altitude' : report.altitude,
        'accuracy' : accuracy
    }

    return render(request, 'report_update.html', context)

# fetch list of reports view
def render_reports_view(request):

    # if user has not logged yet
    if not request.user.is_authenticated:
        return redirect('connection')
    
    # get reports from database
    context = {
        'reports': Report.objects.filter(user=request.user).all()
    }

    return render(request, 'reports.html', context)

# handle delete report request
def render_report_deletion_view(request, id):

    # if user has not logged yet
    if not request.user.is_authenticated:
        return redirect('connection')

    # verify if report exists
    try:
        Report.objects.get(id=id)
    except:
        return HttpResponse(b'<h1>Not Found<h1>', status=404)
    
    # get report from database
    report = Report.objects.get(id=id)

    # verify the creator
    if request.user != report.user:
        return HttpResponse(b'<h1>Permission Denied<h1>', status=403)
    
    # delete report
    report.delete()

    return redirect('reports')
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from basicapp.models import Lobo, User
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

# Create your views here
title = """
<a href="/home"> Where's Lobo? </a>
"""

emailsender = "albertseo@uchicago.edu"

def template(content):
    return f"""
    <html>
    <body>
        {content}
    </body>
    </html>
    """
    
def checkSeen(thisLobo):
    if thisLobo is None:
        reportedLobo = Lobo(location = "", time_seen = timezone.now(), is_claimed = False, claimed_by = "", claim_time = timezone.now())
        reportedLobo.save()
        return "He was not seen..."
    if thisLobo.location != "":
        checktime = thisLobo.time_seen.strftime("%Y-%m-%d %I:%M %p")
        return f"He was seen in {thisLobo.location} at {checktime}"
    return "He was not seen..."

def checkClaim(thisLobo):
    if thisLobo is None:
        return "He's not claimed yet."
    if thisLobo.is_claimed:
        checktime = thisLobo.claim_time.strftime("%Y-%m-%d %I:%M %p")
        return f"He was claimed at {checktime}"
    return "He's not claimed yet."

@csrf_exempt
def index(request):
    global title
    global emailsender
    mydata = Lobo.objects.all()
    if(mydata is None):
        reportedLobo = Lobo(location = "", time_seen = timezone.now(), is_claimed = False, claimed_by = "", claim_time = timezone.now())
        reportedLobo.save()
        mydata = Lobo.objects.all()
    reportedLobo = mydata.last()
    if(request.method == "POST"):
        location = ""
        claimname = ""
        is_claimed = False
        if "location" in request.POST:
            location = request.POST["location"]
            if "claim" in request.POST:
                claimname = request.POST["claim"]
                is_claimed = True
            else:
                is_claimed = False
            reportedLobo = Lobo(location = location, time_seen = timezone.now(), is_claimed = is_claimed, claimed_by = claimname, claim_time = timezone.now())
            reportedLobo.save()
        elif "claim" in request.POST:
            reportedLobo.is_claimed = True
            reportedLobo.claimed_by = request.POST["claim"]
            reportedLobo.claim_time = timezone.now()
            reportedLobo.save()
    report = """
    <form method="POST">
        <input type="text" name="location" placeholder="location">
    </form>
    """
    claim = """
    <form method="POST">
        <input type="text" name="claim" placeholder="name">
    </form>
    """
    page = template(f"""
        <h1> {title} </h1>
        <h3> {checkSeen(reportedLobo)}
        </h3>
        <h3> Claimed?
        {checkClaim(reportedLobo)}!
        </h3>
        <h3>
        Seen him? Where? 
        {report}
        Enter name to claim: {claim}
        </h3>
        <form method="POST">
            <input type="submit">
        </form>
        """)
    return HttpResponse(page)

@csrf_exempt
def signup(request):
    global emailsender
    page = ""
    if(request.method == "POST"):
        if request.POST["Name"] == "":
            page = template("""
                <p> Name empty. Retry.</p>
                Name:
                <input type="text" name="Name" placeholder="Name">
                Email:
                <input type="text" name="Email" placeholder="Email Address">
                <input type="submit">
            """)
            return HttpResponse(page)
        if request.POST["Email"] == "":
            page = template("""
                <p> Email empty. Retry.</p>
                Name:
                <input type="text" name="Name" placeholder="Name">
                Email:
                <input type="text" name="Email" placeholder="Email Address">
                <input type="submit">
            """)
            return HttpResponse(page)
        newUser = User(name=request.POST["Name"], email = request.POST["Email"])
        page = template(f"<h1> {title} </h1> <p> Check Email. Sent to: {newUser.email} </p>")
        send_mail(
            "Signed Up for WheresLobo",
            "Successful signup",
            emailsender,
            [newUser.email],
            fail_silently=False,
        )
        newUser.save()
        return HttpResponse(page)
    page = template(f"""
        <h1> {title} </h1>
        <form method="POST">
            Name:
            <input type="text" name="Name" placeholder="Name">
            email:
            <input type="text" name="Email" placeholder="email address">
            <input type="submit">
        </form>
    """)
    return HttpResponse(page)
    
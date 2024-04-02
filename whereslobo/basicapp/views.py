from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from basicapp.models import Lobo, User
from django.db import models
from django.utils import timezone
from django.shortcuts import redirect

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
        if "location" in request.POST and request.POST["location"] != "":
            location = request.POST["location"]
            if "claim" in request.POST:
                claimname = request.POST["claim"]
                is_claimed = True
            else:
                is_claimed = False
        elif "claim" in request.POST and request.POST["claim"] != "":
            is_claimed = True
            claimname = request.POST["claim"]
        reportedLobo = Lobo(location = location, time_seen = timezone.now(), is_claimed = is_claimed, claimed_by = claimname, claim_time = timezone.now())
        reportedLobo.save()
        redirect("/home")
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

    
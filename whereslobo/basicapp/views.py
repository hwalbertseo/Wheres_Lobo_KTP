from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from basicapp.models import Lobo
from django.db import models
from django.utils import timezone
from django.shortcuts import redirect

# Create your views here
title = """
<a href="/home"> Where's Lobo? </a>
"""

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
        return "He was not seen..."
    if thisLobo.location != "":
        checktime = thisLobo.time_seen.strftime("%Y-%m-%d %I:%M %p")
        return f"He was seen in {thisLobo.location} at {checktime}"
    return "He was not seen..."

def checkClaim(thisLobo):
    return "Test"
    if thisLobo.is_claimed == False:
        return "He's not claimed yet"
    if thisLobo is None or thisLobo.is_claimed == False or thisLobo.claimed_by == "":
        return "He's not claimed yet."
    if thisLobo.is_claimed and thisLobo.claimed_by != "":
        checktime = thisLobo.claim_time.strftime("%Y-%m-%d %I:%M %p")
        return f"He was claimed at {checktime} by {thisLobo.claimed_by}"
    return "He's not claimed yet."

@csrf_exempt
def index(request):
    global title
    reportedLobo = Lobo.objects.last()
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
            location = reportedLobo.location
            claimname = request.POST["claim"]
        if claimname == "":
            is_claimed = False
        if reportedLobo.location != location and location != "":
            reportedLobo = Lobo(location = location, time_seen = timezone.now(), is_claimed = is_claimed, claimed_by = claimname, claim_time = timezone.now())
            reportedLobo.save()
        redirect("/home")
    report = """
    <form method="POST">
        <input type="text" name="location" placeholder="location">
        <p> Enter name to claim: </p>
        <input type="text" name="claim" placeholder="name">
        <p> <input type="submit"> </p>
    </form>
    """
    page = template(f"""
        <h1> {title} </h1>
        Current time: {timezone.now().strftime("%Y-%m-%d %I:%M %p") }
        <h3> {checkSeen(Lobo.objects.last())}
        </h3>
        <h3> Claimed?
        {checkClaim(Lobo.objects.last())}!
        </h3>
        <h3>
        Seen him? Where? 
        {report}
        </h3>
        <p> Directions: You may leave either of the fields blank! </p>
        <ol>
            <li>If you see him, enter the first field.</li>
            <li>If you want to claim the badge at his location, enter the second field.</li>
            <li>If you found him AND claimed him, enter both fields.</li>
        </ol>
        <p> Then press enter! </p>
        Last updated at 4/3/24, 3:35 PM.
        """)
    return HttpResponse(page)

    
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def index(request):
    global title
    location = "Don't Know - Come back soon"
    claimname = ""
    time = f"{0}"
    if(request.method == "POST"):
        if "location" in request.POST:
            location = request.POST["location"]
        elif "claim" in request.POST:
            claimname = request.POST["claim"]
    report = """
    <form method="POST">
        <input type="text" name="location" placeholder="location"> <input type="submit">
    </form>
    """
    claim = """
    <form method="POST">
        <input type="text" name="claim" placeholder="name"> <input type="submit">
    </form>
    """
    claimed = ["No", "Yes"]
    page = template(f"""
        <h1> {title} </h1>
        <h3> He's at:
        {location}!
        </h3>
        <h3> Claimed?:
        {claimed[int(claimname != "")]}!
        </h3>
        <h3>
        Seen him? Where? 
        {report}
        </h3>
        Claim at: {claim}
    """)
    return HttpResponse(page)
    
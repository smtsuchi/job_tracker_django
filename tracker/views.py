from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# models 
from rest_framework.authtoken.models import Token
from .models import Account, Contact, Job
from .serializers import ContactSerializer, JobDescriptionSerializer, JobSerializer, NotesSerializer, RegistrationSerializer

# Create your views here.
@api_view(["GET"])
def index(request):
    return Response({'hello': 'there'})

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getJobs(request):
    user = request.user
    jobs = Job.objects.filter(user=user).order_by('rank')
    columnMap = {'wishlist':[],'applied':[],'interviewing':[],'offer':[]}
    for job in jobs:
        columnMap[job.status].append(job.to_dict())
    return Response(columnMap)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getJob(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)
    if job.user != user:
        print('not matching')
    return Response({"data": job.to_dict(), "job_status": job.status})

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def updateJobs(request):
    user = request.user
    updatedColumnMap = request.data
    if len(updatedColumnMap) == 2:
        jobs = Job.objects.filter(user = user).filter(Q(status=list(updatedColumnMap.keys())[0])|Q(status=list(updatedColumnMap.keys())[1]))
    else:
        jobs = Job.objects.filter(user = user).filter(status=list(updatedColumnMap.keys())[0])
    position = {}
    for category in updatedColumnMap:
        for i, job in enumerate(updatedColumnMap[category]):
            position[job['id']] = {'category':category, "rank":i}
    for job in jobs:
        if job.status != position[str(job.id)]['category'] or job.rank != position[str(job.id)]['rank']:
            job.status = position[str(job.id)]['category']
            job.rank = position[str(job.id)]['rank']
            job.save()
    return Response({'done':'saving'})

@api_view(["POST"])
def registerUser(request):
    serializer = RegistrationSerializer(data = request.data)
    if serializer.is_valid():
        account = serializer.save()
        token = Token.objects.get(user=account).key
        data = {
            'response': "Successfully registered a new user.",
            'email': account.email,
            'username': account.username,
            'token': token,
        }
    else:
        data = serializer.errors
    return Response(data)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addJob(request):
    user = request.user
    job = Job(user=user)
    serializer = JobSerializer(job, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status_code":'success',"data": serializer.data, "obj":job.to_dict()})
    return Response(serializer.errors)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def updateJob(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)
    if user != job.user:
        return Response({"status_code": "error", "message":"You cannot update another user's job."})
    serializer = JobSerializer(job, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status_code":'success',"data": serializer.data, "obj":job.to_dict()})
    return Response(serializer.errors)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def updateJobDescription(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)
    if user != job.user:
        return Response({"status_code": "error", "message":"You cannot update another user's job."})
    serializer = JobDescriptionSerializer(job, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status_code":'success',"data": serializer.data, "obj":job.to_dict()})
    return Response(serializer.errors)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def updateNotes(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)
    if user != job.user:
        return Response({"status_code": "error", "message":"You cannot update another user's job."})
    serializer = NotesSerializer(job, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status_code":'success',"data": serializer.data, "obj":job.to_dict()})
    return Response(serializer.errors)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getJobContacts(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)
    contacts = Contact.objects.filter(job=job_id)
    if user != job.user:
        return Response({"status_code": "error", "message":"You cannot get another user's job."})
    serializer = ContactSerializer(contacts, many=True)
    return Response({"status_code":'success',"data": serializer.data})

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addContact(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)

    if user != job.user:
        return Response({"status_code": "error", "message":"You cannot add to another user's job."})

    contact = Contact(job=job)
    serializer = ContactSerializer(contact, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status_code":'success',"data": serializer.data})
    return Response(serializer.errors)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def updateContact(request, contact_id):
    user = request.user
    contact = Contact.objects.get(id=contact_id)

    if user != contact.job.user:
        return Response({"status_code": "error", "message":"You cannot add to another user's job."})

    serializer = ContactSerializer(contact, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status_code":'success',"data": serializer.data})
    return Response(serializer.errors)
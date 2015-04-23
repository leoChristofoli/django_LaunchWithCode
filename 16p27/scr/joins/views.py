from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from .forms import EmailForm, JoinForm
from .models import Join

def get_ip(request):
	try:
		x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forwarded:
			ip = x_forwarded.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""
	return ip


import uuid

def get_ref_id():
	user_id = uuid.uuid4()
	ref_id = str(user_id)[:11].replace('-','').lower()

	try:
		id_exists = Join.objects.get(ref_id=ref_id)
		#must do something
		#it will be looping until generate a unique id
		get_ref_id()
	except:
		return ref_id



def share(request, ref_id):
	print ref_id
	context  = {"ref_id": ref_id}
	template = "share.html"
	return render(request, template, context)


def home(request):
	try:
		join_id = request.session['join_id_ref']
		obj = Join.objects.get(id=join_id)
	except:
		obj = None

	

	form = JoinForm(request.POST or None)
	if form.is_valid():
		new_join = form.save(commit = False)
		#do something here
		email = form.cleaned_data['email']
		new_join_old, created = Join.objects.get_or_create(email=email)
		if created:
			new_join_old.ref_id = get_ref_id()
			#add our friend who referred us
			if not obj == None:
				new_join_old.friend = obj
			new_join_old.ip_address = get_ip(request)
			new_join_old.save()
		
		#print all friends
		print Join.objects.filter(friend=obj).count()
		print obj.referral.all().count()


		#redirect here
		return HttpResponseRedirect("/%s" %(new_join_old.ref_id))

	context  = {"form": form}
	template = "home.html"
	return render(request, template, context)
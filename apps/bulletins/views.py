from django.shortcuts import redirect, render
from django.views.generic import *
from formtools.wizard.views import *
from django.http import *

from .forms import *
from .models import Bulletin

from django.views.generic.edit import FormView


from .forms import *
from .models import Bulletin




class BulletinListView(ListView):
    model = Bulletin
    template_name = 'bulletins/bulletin_list.html'


class BulletinDetailView(View):
    def get(self, request, bulletin_id):
        bulletin = Bulletin.objects.get(id=bulletin_id)
        return render(request, 'bulletins/bulletin_detail.html', {'bulletin': bulletin})

class CreateBulletinView(View):
    def get(self, request):
        form = BulletinForm()
        return render(request, 'bulletins/create_bulletin.html', {'form': form})

    def post(self, request):
        form = BulletinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bulletins:list')
        return render(request, 'bulletins/create_bulletin.html', {'form': form})

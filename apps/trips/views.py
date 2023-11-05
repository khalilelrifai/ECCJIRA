
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import *
from xhtml2pdf import pisa

from .forms import *
from .models import *


class ExportTripsAsPDFView(TemplateView):
    template_name = 'trips/trip_list_pdf.html'

    def get(self, request, *args, **kwargs):
        trips = self.kwargs.get('trips', [])

        context = {'trips': trips}
        template = get_template(self.template_name)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="trips.pdf"'

        pisa_status = pisa.CreatePDF(
            html, dest=response, encoding='utf-8')

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response


class CreateTripView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trips/trip_form.html'
    form_class = CreateTripForm

    success_url = reverse_lazy('trips:main')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TripListView(LoginRequiredMixin, View):
    template_name = 'trips/trip_list.html'
    model = Trip
    paginate_by = 10

    def get(self, request):
        
        form = TripFilterForm(request.GET)
        if form.is_valid():
            trips = form.filter_trips().order_by('-created_at')
            if 'export' in request.GET:
                pdf_view = ExportTripsAsPDFView.as_view()
                response = pdf_view(request, trips=trips)
                return response
                  

        else:
            trips = Trip.objects.none()
      
            
        paginator = Paginator(trips, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        context = {'form': form, 'page_obj': page_obj}
        return render(request, self.template_name, context)







class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    
    

class TripRequest(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'trips/trip_request.html'

    def test_func(self):
        # Check if the user is a Security user
        return self.request.user.security is not None

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(
            vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            return render(request, self.template_name, {'trip': last_trip})
        else:
            raise Http404('No trips found for this vehicle')

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(
            vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            action = request.POST.get('action')
            
            if action == 'approve' and last_trip.check_out is not None:
                last_trip.check_in = timezone.now()
                last_trip.status = 'Closed'
                last_trip.save()
                return redirect('trips:trip_request', pk=vehicle.pk)
            elif action == 'approve':
                last_trip.approval_request = 'Approved'
                last_trip.verified_by = request.user.security
                last_trip.check_out = timezone.now()
                last_trip.save()
                return redirect('trips:trip_request', pk=vehicle.pk)
            elif action == 'reject':
                last_trip.approval_request = 'Rejected'
                last_trip.verified_by = request.user.security
                last_trip.save()
                return redirect('trips:trip_request', pk=vehicle.pk)
            elif action == 'cancel':
                return redirect('trips:list')
            else:
                return HttpResponseBadRequest('Invalid action')
        else:
            raise Http404('No trips found for this vehicle')

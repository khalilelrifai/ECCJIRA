from django.shortcuts import render, redirect
from .forms import VideoForm
from ftplib import FTP
from django.conf import settings
from .models import *
from django.contrib.auth.decorators import permission_required
import os
from django.views.generic import *
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
import time
from django.http import JsonResponse

from django.shortcuts import render, redirect

@permission_required('assignment.upload_video')
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.owner = request.user
            video.upload_status = 'Uploading...'
            video.save()

            try:
                # Upload the video file to the FTP server
                with FTP(settings.FTP_HOST) as ftp:
                    ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
                    ftp.cwd(settings.FTP_UPLOAD_DIR)

                    # Get the title from the form
                    title = form.cleaned_data['title']
                    file = request.FILES['file']

                    # Generate new file name using the title
                    new_file_name = f'{title}'

                    ftp.cwd('videos')

                    # Check if upload was interrupted
                    if video.upload_progress > 0:
                        resume_position = int(video.upload_progress * file.size)
                        file.seek(resume_position)

                    # Read and upload the file in chunks
                    chunk_size = 64 * 1024  # 64KB
                    total_size = file.size
                    bytes_uploaded = 0
                    start_time = time.time()
                    with file.open('rb') as file_stream:
                        while True:
                            if video.is_paused:
                                # Update the video object with paused status
                                video.upload_status = 'Upload paused'
                                video.save()
                                return redirect('assignment:my_list')

                            chunk = file_stream.read(chunk_size)
                            if not chunk:
                                break
                            ftp.storbinary(f'APPE {new_file_name}', ContentFile(chunk))
                            bytes_uploaded += len(chunk)
                            video.upload_progress = bytes_uploaded / total_size

                            # Calculate progress and estimated time
                            elapsed_time = time.time() - start_time
                            if video.upload_progress > 0:
                                estimated_time = elapsed_time / video.upload_progress - elapsed_time
                            else:
                                estimated_time = 0

                            # Update the video object with progress and estimated time
                            video.upload_status = f'Uploading... Progress: {video.upload_progress:.2%}. Megabytes Uploaded: {bytes_uploaded / (1024 * 1024):.2f}/{total_size / (1024 * 1024):.2f}. Estimated time: {estimated_time:.2f}s'
                            video.save()

                    # Update the video object after successful upload
                    video.upload_status = 'Uploaded successfully!'
                    video.upload_progress = 1
                    video.save()
                    return redirect('assignment:my_list')

            except Exception as e:
                # Update the video object with the error status
                video.upload_status = f'Upload failed: {str(e)}'
                video.save()
                return redirect('assignment:video_list')

    else:
        form = VideoForm()

    return render(request, 'assignment/upload.html', {'form': form})





def ftp_list():
    try:
        ftp = FTP(settings.FTP_HOST)
        ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
        ftp.cwd(settings.FTP_UPLOAD_DIR)
        files_List = [file_name.replace('videos/', '').split('.')[0] for file_name in ftp.nlst('videos/')]
        ftp.quit()
    except Exception as e:
        # Handle FTP connection or error exception here
        return False
    
    return files_List



def video_exist():
    videos = Video.objects.all()
    list = ftp_list()
    for video in videos:
        if video.title in list:
            video.ftp_exists = True
        else:
            video.ftp_exists = False
        video.save()



# class VideoListView(View):
#     template_name = 'assignment/list.html'
#     paginate_by = 10

#     def get(self, request):
#         strval = request.GET.get("search", False)
#         video_exist()
#         if request.user.is_authenticated:
#             if strval:
#                 query = Q(description__icontains=strval)
#                 query.add(Q(title__icontains=strval), Q.OR)

#                 video_list = Video.objects.filter(query).select_related().order_by('-uploaded_at')
#             else:
#                 video_list = Video.objects.all().order_by('-uploaded_at')
                
#             paginator = Paginator(video_list, self.paginate_by)
#             page_number = request.GET.get('page')
#             page_obj = paginator.get_page(page_number)
            
#             context = {

#                 'page_obj':page_obj,
#                 'search': strval,
#             }

#             return render(request, self.template_name, context)
        
class VideoListView(PermissionRequiredMixin,ListView):
    permission_required = 'assignment.admin_user'
    model = Video
    template_name = 'assignment/list.html'
    context_object_name = 'videos'
    paginate_by = 10
    def get_queryset(self):
        if video_exist():
            video_exist()
        else:
            pass
        
        queryset = super().get_queryset()
        queryset = queryset.filter().order_by('-uploaded_at')
        return queryset


class OwnerVideoListView(PermissionRequiredMixin,ListView):
    permission_required = 'assignment.normal_user'
    model = Video
    template_name = 'assignment/list.html'
    context_object_name = 'videos'
    paginate_by = 10
    def get_queryset(self):
        if video_exist():
            video_exist()
        else:
            pass
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user).order_by('-uploaded_at')
        return queryset
        
class VideoDetailView(PermissionRequiredMixin,DetailView):
    permission_required = 'assignment.normal_user'
    model = Video
    template_name= "assignment/video_detail.html"
    
    
    




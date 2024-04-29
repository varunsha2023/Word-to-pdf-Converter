from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pdf2image import convert_from_path

from .models import PDFFile

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_url = fs.url(filename)

        # Convert PDF to JPG
        images = convert_from_path(settings.MEDIA_ROOT + uploaded_file_url)
        
        # Save JPG images
        for i, image in enumerate(images):
            image.save(settings.MEDIA_ROOT + f'pdf_images/page_{i}.jpg')

        return render(request, 'converter/upload_pdf.html', {
            'uploaded_file_url': uploaded_file_url,
            'images': images
        })
    return render(request, 'converter/upload_pdf.html')

def home(request):
    return render(request, 'converter/home.html')

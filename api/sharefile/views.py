from django.shortcuts import render

from sharefile.models import ShareFile

def friendFiles(request):
    fileList = ShareFile.objects.get(email=email)
    context = {'fileList': fileList}
    return render(request, 'sharefile/friendFiles.html', context)


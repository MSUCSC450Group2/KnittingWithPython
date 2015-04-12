from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from .forms import *
from .manipulate_lib.imageclass import *
from .models import Image
from image_manipulation.models import Image
import time

def applicationPage():
    return 'image_manipulation/applicationPage.html'

def newUploadedImage(request):
    return Image(imgFile = request.FILES['imgFile'], user = request.user, 
                 private = True)

def imageUpload(request):
    imgForm = ImageUploadForm(request.POST, request.FILES)
    if "required" in str(imgForm['imgFile'].errors): # for when no image is uploaded
        imgForm = ImageUploadForm()
    elif imgForm.is_valid():
        newImg = newUploadedImage(request)
        newImg.save()
    return imgForm
   
def saveFormDataToCookie(form, response):
    setCookie(response, 'numberOfColors', int(form.cleaned_data['numberOfColors']))
    setCookie(response, 'guageSize', float(form.cleaned_data['guageSize']))
    setCookie(response, 'canvasLength', float(form.cleaned_data['canvasLength']))
    setCookie(response, 'canvasWidth', float(form.cleaned_data['canvasWidth']))
    setCookie(response, 'knitType', int(form.cleaned_data['knitType']))

def isSavedCookieData(request):
    return ('numberOfColors' in request.COOKIES) if True else False

def getSavedCookieData(request):
    return ManipulateImageForm( {
        'numberOfColors':int(request.COOKIES['numberOfColors']),
        'guageSize':float(request.COOKIES['guageSize']),
        'canvasLength':float(request.COOKIES['canvasLength']),
        'canvasWidth':float(request.COOKIES['canvasWidth']),
        'knitType':int(request.COOKIES['knitType'])
    } )

def saveFormDataToSession(form, request):
    request.session.set_expiry(31536000) # one year
    request.session['savedFormOptions'] = {
        'numberOfColors': int(form.cleaned_data['numberOfColors']), 
        'guageSize': float(form.cleaned_data['guageSize']), 
        'canvasLength': float(form.cleaned_data['canvasLength']),
        'canvasWidth': float(form.cleaned_data['canvasWidth']), 
        'knitType': int(form.cleaned_data['knitType'])
    }

def isSavedSessionData(request):
    return request.session.get('savedFormOptions')

def savedSessionData(savedOptions):
    return ManipulateImageForm(
            {'numberOfColors': int(savedOptions.get('numberOfColors')),
             'guageSize': float(savedOptions.get('guageSize')),
             'canvasLength': float(savedOptions.get('canvasLength')),
             'canvasWidth': float(savedOptions.get('canvasWidth')),
             'knitType': int(savedOptions.get('knitType')) }
           )

def setCookie(response, key, value, days_expire = 365):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60 

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(key, value, max_age=max_age, expires=expires)

def deleteCookie(response):
    response.delete_cookie('savedFormOptions')

@login_required
def fetchApplication(request):
    inputImage = Image.latestUserImageFile(request.user)
    resultImage = 'media/result.jpg'
    requestImage = inputImage

    if request.method == 'POST':
        form = ManipulateImageForm(request.POST) 
        if form.is_valid():
            requestImage = "../" + resultImage # django is preappending /media
            numColors = form.cleaned_data['numberOfColors']
            pixSize = 8
            pic = Picture(inputImage)
            pic.pixelate(numColors, pixSize, resultImage)
            cookieAction = 0;
        else:
            cookieAction = 1
    else:
        cookieAction = 1

    # Load saved cookie data if available
    if cookieAction == 1:
        if isSavedCookieData(request):
            form = getSavedCookieData(request)
        else:
            form  = ManipulateImageForm()

    response = render_to_response(applicationPage(), {
                              'imgForm': imageUpload(request),
                              'form': form,
                              'image': requestImage },
                              context_instance = RequestContext(request))

    # Save any valid data to cookie
    if cookieAction == 0:
        saveFormDataToCookie(form, response)
    return response

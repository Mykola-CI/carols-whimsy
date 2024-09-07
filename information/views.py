from django.shortcuts import render


def about(request):
    """ A view to return the about us page """

    return render(request, 'information/about_us.html')


def contacts(request):
    """ A view to return the contacts page """

    return render(request, 'information/contacts.html')


def faq(request):
    """ A view to return the faq page """

    return render(request, 'information/faq.html')
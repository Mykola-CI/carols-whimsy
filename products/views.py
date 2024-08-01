from django.shortcuts import render


def catalog(request):
    """ A view to return the catalog page """

    return render(request, 'products/catalog.html')

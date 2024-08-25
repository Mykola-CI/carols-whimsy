from .models import Brand, Category, Theme, Season


def product_categories(request):
    """
    Product categories context processor so our Product categories
    can be available in all templates across the site
    """
    brands = Brand.objects.all()
    categories = Category.objects.all()
    themes = Theme.objects.all()
    seasons = Season.objects.all()

    context = {
        'brands': brands,
        'categories': categories,
        'themes': themes,
        'seasons': seasons,
    }

    return context

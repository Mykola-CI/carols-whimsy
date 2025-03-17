from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .cart import Cart
from products.models import Product, Brand, Category, Theme, Season
from .forms import PromoCodeForm
from vendor.models import CommercialConstant, PromoCodeUsage


def cart_summary(request):
    """
    Summary view of the cart
    Return: render the cart summary template
    """

    if request.method == "POST":
        # Check if User is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to use a promo code.")
            return redirect("cart_summary")

        form = PromoCodeForm(request.POST)
        if form.is_valid():
            promo_code = form.cleaned_data["promo_code"]

            if PromoCodeUsage.objects.filter(
                user=request.user, promo_code=promo_code
            ).exists():
                messages.error(request, "You have already used this promo code.")
                # Reset discount in the session to ensure it's not used within
                # the same session twice after the first order completion
                request.session["promo_discount"] = 0
            else:
                try:
                    promo = CommercialConstant.objects.get(friendly_name=promo_code)
                    request.session["promo_discount"] = promo.value
                    PromoCodeUsage.objects.create(
                        user=request.user, promo_code=promo_code
                    )

                    messages.success(
                        request,
                        "Promo code applied! You get a discount of "
                        + f"{promo.value}%.",
                    )
                except CommercialConstant.DoesNotExist:
                    messages.error(request, "Invalid promo code.")

            return redirect("cart_summary")
    else:
        form = PromoCodeForm()

    # Calculation of amount left to free delivery
    cart = Cart(request)
    totals = cart.get_totals
    threshold = CommercialConstant.objects.get(
        name="free_delivery_threshold"
    ).get_value()
    if totals < threshold:
        left_to_free_delivery = round((threshold - totals), 2)
        percent_of_threshold = round(((totals / threshold) * 100), 2)
    else:
        left_to_free_delivery = 0
        percent_of_threshold = 100

    brands = Brand.objects.all()
    categories = Category.objects.all()
    themes = Theme.objects.all()
    seasons = Season.objects.all()
    products = Product.objects.all()

    context = {
        "brands": brands,
        "categories": categories,
        "themes": themes,
        "seasons": seasons,
        "products": products,
        "form": form,
        "left_to_free_delivery": left_to_free_delivery,
        "percent_of_threshold": percent_of_threshold,
    }

    return render(request, "cart/cart_summary.html", context)


@require_POST
def add_to_cart(request):
    """
    Add a product to the cart
    """

    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity", 1)

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1  # Ensure minimum quantity is 1
    except (ValueError, TypeError):
        quantity = 1  # Default to 1 if invalid

    # Just checking if the product exists, if not, return a 404
    product = get_object_or_404(Product, pk=product_id)

    try:
        cart = Cart(request)

        cart_quantity = cart.cart.get(str(product_id), 0)
        if quantity > (product.stock - cart_quantity):
            messages.error(
                request,
                f"Cannot add {quantity} item(s) of \"{product.name}\""
                f" to your cart. "
                f"Only {product.stock} item(s) available in stock."
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"status": "error"}, status=400)
            else:
                return HttpResponseRedirect(request.META.get(
                    "HTTP_REFERER", "/"))

        cart.add(product=product, quantity=quantity)

        messages.success(
            request,
            f"Added ({quantity}) item(s) of "
            f'"{product.name}" to your cart. '
            f"Click on the Cart button to view your cart.",
        )

    except Exception as _:
        messages.error(request, "There was an error adding the product to your cart.")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "error"}, status=500)
        else:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"status": "success"})
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def update_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        new_quantity = int(request.POST.get("quantity"))

        # Check if the product exists
        product = get_object_or_404(Product, pk=product_id)

        cart = Cart(request)
        # Retrieve the old quantity for the product before the update
        old_quantity = cart.cart.get(str(product_id), 0)

        if new_quantity > product.stock:
            messages.error(
                request,
                f"Cannot add {new_quantity} item(s) of \"{product.name}\""
                f" to your cart. "
                f"Only {product.stock} item(s) available in stock."
            )
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"status": "error"}, status=400)
            else:
                return HttpResponseRedirect(request.META.get(
                    "HTTP_REFERER", "/"))

        # Update the product quantity in the cart
        cart.update(product=product, quantity=new_quantity)

        messages.success(
            request,
            f'Updated quantity of "{product.name}" from '
            f"({old_quantity}) to ({new_quantity}). "
            f"Click on the Cart button to view your cart.",
        )

        return JsonResponse({"status": "success"}, status=200)


def remove_item(request, product_id):

    cart = Cart(request)
    product_item = get_object_or_404(Product, pk=product_id)
    name = product_item.name
    cart.delete_item(product_id)

    messages.info(request, f'Removed "{name}" from cart.')

    return redirect("cart_summary")


def clear_cart(request):

    cart = Cart(request)
    cart.clear()

    messages.info(request, "Cart has been cleared.")

    return redirect("cart_summary")

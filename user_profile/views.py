from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from allauth.account.models import EmailAddress

from .models import UserProfile, ShippingAddress, Wishlist
from checkout.models import OrderLineItem
from products.models import Product
from cart.cart import Cart
from .forms import (
    BasicUserInfoForm, PhoneNumberForm, EmailForm,
    CustomPasswordChangeForm, ShippingAddressForm)


@login_required
def view_user_profile(request):
    # Get the currently authenticated user
    user = request.user

    # Retrieve the associated UserProfile instance
    user_profile = get_object_or_404(UserProfile, user=user)
    title_readable = user_profile.get_title_readable()
    orders = user_profile.orders.all()

    # Count the number of orders
    order_count = orders.count()

    form_basic = BasicUserInfoForm(instance=user_profile, user=user)
    form_phone = PhoneNumberForm(instance=user_profile)
    form_email = EmailForm(instance=user)
    form_password = CustomPasswordChangeForm(user=user)

    template = 'user_profile/view-profile.html'
    context = {
        'user_profile': user_profile,
        'title_readable': title_readable,
        'form_basic': form_basic,
        'form_phone': form_phone,
        'form_email': form_email,
        'form_password': form_password,
        'order_count': order_count,
    }

    return render(request, template, context)


@login_required
@require_POST
def update_user_basic_info(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    form_basic = BasicUserInfoForm(
        request.POST, instance=user_profile, user=user)
    if form_basic.is_valid():
        form_basic.save()  # Save the updated form data

        # Refresh the User instance from the database to get the latest data
        # before sending it back to the client, otherwise the first_name
        # and the last_name are not updated by front end JavaScript
        user.refresh_from_db()

        # Prepare the updated data to send back
        updated_data_basic = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user_profile.profile_date_of_birth,
            'title': user_profile.get_title_readable(),
        }
        message = 'Your account has been updated.'
        success = True

    else:
        updated_data_basic = {}
        message = 'Failed to update account. Please try again.'
        success = False

    return JsonResponse({
        'success': success,
        'updated_basic': updated_data_basic,
        'errors': form_basic.errors if not success else {},
        'message': message
    })


@login_required
@require_POST
def update_user_phone(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    form_phone = PhoneNumberForm(
        request.POST, instance=user_profile)
    if form_phone.is_valid():
        form_phone.save()  # Save the updated form data

        # Re-fetch the user object to get the updated email
        user_profile.refresh_from_db()

        message = 'Your phone number has been updated.'
        success = True

    else:
        message = 'Failed to update phone number. Please try again.'
        success = False

    return JsonResponse({
        'success': success,
        'message': message,
        'updated_phone': user_profile.profile_phone_number})


@login_required
def change_email(request):
    """ A view to handle the email change request """

    if request.method == 'POST':
        new_email = request.POST.get('email')
        user = request.user

        # Check if the email is already in use
        if EmailAddress.objects.filter(email=new_email).exists():

            return JsonResponse(
                {'success': False,
                 'message': 'This email is already in use.'},
                status=200)

        # Ensure no other email is marked as primary
        EmailAddress.objects.filter(
            user=user, primary=True).update(primary=False)

        # Add the new email and send confirmation
        email_address, created = EmailAddress.objects.get_or_create(
            user=user,
            email=new_email,
            defaults={'verified': False, 'primary': True}
        )

        # Send confirmation email calling the method of the django-allauth's
        #  EmailAddress object. Upon confirmation the new email is set
        #  as 'verified' in Email addresses and saved to User model.
        if created or not email_address.verified:
            email_address.send_confirmation(request)
            return JsonResponse({
                'success': True,
                'message': 'Email change request sent. Please check your email'
                           ' for confirmation.'
                           ' Your new email must be verified.'
            })
        else:
            return JsonResponse(
               {'success': False,
                'message': 'This email is already associated with '
                           'your account.'},
               status=200
            )

    return JsonResponse(
        {'success': False, 'message': 'Invalid request method.'}, status=400)


@login_required
@require_POST
def change_password(request):
    """ A view to handle POST requests for the password change form """

    # if request.method == 'POST':
    form = CustomPasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        # Important to keep the user logged in after password change
        update_session_auth_hash(request, form.user)
        messages.success(
            request, 'Your password was successfully updated!')
        return redirect('view_profile')
    else:
        messages.error(request, 'Please correct the error or try again.')
        return redirect('view_profile')


@login_required
def view_order_history(request):
    ''' A view to display the order history of the user '''

    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    # Count the number of orders
    order_count = orders.count()

    # Create a dictionary to hold orders and their line items
    orders_with_items = []
    for order in orders:
        line_items = OrderLineItem.objects.filter(order=order)
        orders_with_items.append({
            'order': order,
            'line_items': line_items
        })

    template = 'user_profile/order-history.html'

    context = {
        'orders_with_items': orders_with_items,
        'order_count': order_count
    }

    return render(request, template, context)


@login_required
def delete_user_account(request):
    """ A view to delete the user account """

    user = request.user
    user.delete()
    messages.info(request, 'Your account has been deleted.')
    return redirect('home')


@login_required
def set_shipping_details_profile(request):
    """ A view to manage shipping addresses """
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    shipping_addresses = ShippingAddress.objects.filter(
        user_profile=user_profile)

    if request.method == 'POST':
        # Determine if we are editing an existing address or adding a new one
        address_id = request.POST.get('address_id')
        if address_id:
            # Editing an existing address
            shipping_address = get_object_or_404(
                ShippingAddress, id=address_id, user_profile=user_profile)
            shipping_address_form = ShippingAddressForm(
                request.POST, instance=shipping_address)
        else:
            # Adding a new address
            shipping_address_form = ShippingAddressForm(request.POST)

        if shipping_address_form.is_valid():
            shipping_address = shipping_address_form.save(commit=False)
            shipping_address.user_profile = user_profile  # Associate the user
            shipping_address.save()

            messages.success(
                request, 'The shipping address added successfully.')
            return redirect('manage_shipping_addresses')
    else:
        shipping_address_form = ShippingAddressForm()

    template = 'user_profile/shipping-addresses.html'
    context = {
        'shipping_address_form': shipping_address_form,
        'shipping_addresses': shipping_addresses,
    }

    return render(request, template, context)


@login_required
def get_address_data(request):
    """ A view to get the existing address data for editing """
    address_id = request.GET.get('address_id')
    shipping_address = get_object_or_404(
        ShippingAddress, id=address_id, user_profile=request.user.userprofile)

    data = {
        'delivery_first_name': shipping_address.delivery_first_name,
        'delivery_last_name': shipping_address.delivery_last_name,
        'delivery_phone_number': shipping_address.delivery_phone_number,
        'delivery_email': shipping_address.delivery_email,
        'shipping_street_address': shipping_address.shipping_street_address,
        'shipping_town_city': shipping_address.shipping_town_city,
        'shipping_county': shipping_address.shipping_county,
        'shipping_postcode': shipping_address.shipping_postcode,
        'shipping_country': shipping_address.shipping_country.code,
    }

    return JsonResponse(data)


@login_required
@require_POST
def edit_shipping_addresses_profile(request, address_id):
    """ A view to edit a shipping address """
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    shipping_address = get_object_or_404(
        ShippingAddress, id=address_id, user_profile=user_profile)

    shipping_address_form = ShippingAddressForm(
        request.POST, instance=shipping_address)

    if shipping_address_form.is_valid():
        shipping_address_form.save()
        messages.success(request, 'The shipping address updated successfully.')
        return redirect('manage_shipping_addresses')
    else:
        messages.error(request, 'Failed to update address. Please try again.')
        return redirect('manage_shipping_addresses')


@login_required
def delete_address(request, address_id):
    """ A view to delete a shipping address """

    shipping_address = get_object_or_404(
        ShippingAddress, id=address_id, user_profile=request.user.userprofile)
    shipping_address.delete()

    messages.info(request, 'The shipping address has been deleted.')
    return redirect('manage_shipping_addresses')


@login_required
def wishlist_view(request):
    ''' A view to display and manipulate the wishlist of the user '''

    # Provide the order count context for the aside panel of the page
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    # Count the number of orders
    order_count = orders.count()

    # Get the wishlist for the user
    wishlist = get_object_or_404(Wishlist, user=request.user)

    template = 'user_profile/view-wishlist.html'

    context = {
        'wishlist': wishlist,
        'order_count': order_count
    }

    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id):
    """ A view to add a product to the user's wishlist """

    product = get_object_or_404(Product, id=product_id)

    # Get the wishlist for the user
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.add(product)

    messages.success(request, f'"{product.name}" added to your wishlist')

    return redirect(reverse('product_detail', args=[product_id]))


@login_required
def remove_wishlist_items(request):
    """ A view to remove items from the user's wishlist """

    # Get the user's wishlist
    wishlist = get_object_or_404(Wishlist, user=request.user)

    # Check if the request method is POST
    if request.method == 'POST':
        # Get the list of product IDs to remove from the wishlist
        product_ids = request.POST.getlist('product_ids')

        if not product_ids:
            messages.error(
                request, 'No items selected to remove from wishlist')
            return redirect('wishlist')
        # Remove the products from the wishlist
        for product_id in product_ids:
            product = get_object_or_404(Product, id=product_id)
            wishlist.products.remove(product)

        messages.success(request, 'Selected items removed from your wishlist')
        # Redirect back to the wishlist view
    return redirect('wishlist')


@login_required
def add_to_cart_from_wishlist(request, product_id):
    """ A view to add a product to the cart from the wishlist """

    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product, quantity=1)
    messages.success(
        request, f'Added "{product.name}" to your cart. '
                 f'Click on the Cart button to view your cart'
                 f' and update the quantity if needed.')
    return redirect('wishlist')

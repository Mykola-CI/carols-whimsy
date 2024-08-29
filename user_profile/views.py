from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from allauth.account.models import EmailAddress

from .models import UserProfile
from checkout.models import OrderLineItem
from .forms import (
    BasicUserInfoForm, PhoneNumberForm, EmailForm, CustomPasswordChangeForm)


@login_required
def view_user_profile(request):
    # Get the currently authenticated user
    user = request.user

    # Retrieve the associated UserProfile instance
    user_profile = get_object_or_404(UserProfile, user=user)
    title_readable = user_profile.get_title_readable()

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
    }

    return render(request, template, context)


@login_required
@require_POST
def update_user_basic_info(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    form_basic = BasicUserInfoForm(request.POST, instance=user_profile, user=user)
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
        return JsonResponse(
            {'success': True, 'updated_basic': updated_data_basic})
    else:
        return JsonResponse({'success': False, 'errors': form_basic.errors})


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

        return JsonResponse(
            {'success': True,
             'updated_phone': user_profile.profile_phone_number})
    else:
        return JsonResponse({'success': False, 'errors': form_phone.errors})


@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        user = request.user

        # Check if the email is already in use
        if EmailAddress.objects.filter(email=new_email).exists():
            return JsonResponse(
                {'error': 'This email is already in use.'}, status=400)

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
            return JsonResponse({'success': 'Email change request sent. ' +
                                 'Please check your email for confirmation.'})
        else:
            return JsonResponse(
                {'error': 'This email is already associated '
                 + 'with your account.'},
                status=400
            )

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def change_password(request):
    """ A view to handle POST requests for the password change form """

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Important to keep the user logged in after password change
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('view_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def view_order_history(request):
    ''' A view to display the order history of the user '''

    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    # Create a dictionary to hold orders and their line items
    orders_with_items = []
    for order in orders:
        line_items = OrderLineItem.objects.filter(order=order)
        orders_with_items.append({
            'order': order,
            'line_items': line_items
        })

    template = 'user_profile/order-history.html'

    return render(request, template, {'orders_with_items': orders_with_items})


@login_required
def delete_user_account(request):
    """ A view to delete the user account """

    user = request.user
    user.delete()
    messages.success(request, 'Your account has been deleted.')
    return redirect('home')

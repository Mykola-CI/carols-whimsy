from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import UserProfile
from .forms import BasicUserInfoForm


@login_required
def view_user_profile(request):
    # Get the currently authenticated user
    user = request.user

    # Retrieve the associated UserProfile instance
    user_profile = get_object_or_404(UserProfile, user=user)
    title_readable = user_profile.get_title_readable()

    form = BasicUserInfoForm(instance=user_profile, user=user)

    template = 'user_profile/view-profile.html'
    context = {
        'user_profile': user_profile,
        'title_readable': title_readable,
        'form': form,
    }

    return render(request, template, context)


@login_required
@require_POST
def update_user_basic_info(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    form = BasicUserInfoForm(request.POST, instance=user_profile, user=user)
    if form.is_valid():
        form.save()  # Save the updated form data
        # Prepare the updated data to send back
        updated_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user_profile.profile_date_of_birth,
            'title': user_profile.get_title_readable(),
        }
        return JsonResponse({'success': True, 'updated_data': updated_data})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

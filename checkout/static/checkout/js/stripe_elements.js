$(document).ready(function () {
    const stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
    const clientSecret = $('#id_client_secret').text().slice(1, -1);

    const stripe = Stripe(stripe_public_key);

    const appearance = {
        theme: 'flat',
        variables: { colorPrimaryText: '#262626' }
    };
    const options = {
        layout: {
            type: 'tabs',
            defaultCollapsed: false,
        }
    };
    const elements = stripe.elements({ clientSecret, appearance });
    const paymentElement = elements.create('payment', options);
    paymentElement.mount('#payment-element');

    // Handle realtime validation errors on the payment element
    paymentElement.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
            <span class="icon" role="alert">
                <i class="fa-regular fa-triangle-exclamation"></i>
            </span>
            <span>${event.error.message}</span>
        `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    // Handle form submit
    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        paymentElement.update({ 'disabled': true });
        $('#complete-order').attr('disabled', true);

        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
        };
        var url = '/checkout/cache_checkout_data/';

        $.post(url, postData).done(function () {
            stripe.confirmPayment({
                elements,
                confirmParams: {
                    return_url: `${window.location.origin}/checkout/confirmation/`
                },
                redirect: 'if_required'
                // Return a promise that resolves when the payment is successful
            }).then(function (result) {
                if (result.error) {
                    var errorDiv = document.getElementById('card-errors');
                    var html = `
                <span class="icon" role="alert">
                <i class="fa-regular fa-triangle-exclamation"></i>
                </span>
                <span>${result.error.message}</span>`;
                    $(errorDiv).html(html);
                    paymentElement.update({ 'disabled': false });
                    $('#complete-order').attr('disabled', false);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        });
    });
});

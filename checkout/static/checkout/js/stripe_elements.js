// const stripe_public_key = document.getElementById('id_stripe_public_key').innerText.slice(1, -1);
// const clientSecret = document.getElementById('id_client_secret').innerText.slice(1, -1);

// const stripe = Stripe(stripe_public_key);

// const appearance = {
//     theme: 'flat',
//     variables: { colorPrimaryText: '#262626' }
// };
// const options = {
//     layout: {
//         type: 'tabs',
//         defaultCollapsed: false,
//     }
// };
// const elements = stripe.elements({ clientSecret, appearance });
// const paymentElement = elements.create('payment', options);
// paymentElement.mount('#payment-element');

$(document).ready(function() {
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
});
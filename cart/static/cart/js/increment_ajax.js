// The script below is used to increment and decrement the quantity of a product in the cart
// and submits new quantities the view using AJAX.

$(document).ready(function () {
    // Decrement quantity
    $('.cart-btn-decrement').on('click', function () {
        var $input = $(this).siblings('.cart-qty-input');
        var currentQuantity = parseInt($input.val());
        var productId = $(this).closest('.count-input').data('product-id');

        if (currentQuantity > 1) {
            $input.val(currentQuantity - 1);
            updateCart(productId, $input.val());
        }
    });

    // Increment quantity
    $('.cart-btn-increment').on('click', function () {
        var $input = $(this).siblings('.cart-qty-input');
        var currentQuantity = parseInt($input.val());
        var productId = $(this).closest('.count-input').data('product-id');

        $input.val(currentQuantity + 1);
        updateCart(productId, $input.val());
    });

    // Function to send AJAX request
    function updateCart(productId, newQuantity) {
        $.ajax({
            url: '/cart/update/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken, // Ensure CSRF token is included
                'product_id': productId,
                'quantity': newQuantity
            },

            success: function (response) {
                // Handle success (e.g., update cart total, display message)
                window.location.reload();
            },
            error: function (xhr, status, error) {
                // Handle error
                console.error('Error updating cart:', error);
            }
        });
    }
});

$(document).ready(function () {
    // Show/hide buttons based on scroll position
    $(window).on('scroll', function () {
        var scrollTop = $(this).scrollTop();
        var docHeight = $(document).height();
        var windowHeight = $(this).height();

        // Show "Top" button if scrolled down
        if (scrollTop > 100) {
            $('.btn-scroll[href="#top"]').addClass('show');
        } else {
            $('.btn-scroll[href="#top"]').removeClass('show');
        }

        // Show "Bottom" button if not at the bottom
        if (scrollTop + windowHeight < docHeight - 100) {
            $('.btn-scroll[href="#bottom"]').addClass('show');
        } else {
            $('.btn-scroll[href="#bottom"]').removeClass('show');
        }

        // Check if near the bottom of the page
        if (scrollTop + windowHeight >= docHeight - 100) {
            $('.btn-scroll').addClass('white-text');
        } else {
            $('.btn-scroll').removeClass('white-text');
        }

    });

    // Trigger scroll event on page load to set initial button visibility
    $(window).trigger('scroll');
});

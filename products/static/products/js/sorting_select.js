// Replace the URL with the current URL and add the sorting parameter to the URL

$(document).ready(function () {
    $('.sorting-select').change(function () {
        var selector = $(this);
        var currentUrl = new URL(window.location);

        var selectedVal = selector.val();
        if (selectedVal != "reset") {
            currentUrl.searchParams.set("sort", selectedVal);
        } else {
            currentUrl.searchParams.delete("sort");
        }
        window.location.replace(currentUrl);
    });
});
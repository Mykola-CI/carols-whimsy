# TESTING
## Validation

### HTML validation

No errors found in my html. This checking was done manually by copying the view page source code and pasting it into the validator.
There are warnings though, all of them being "The type attribute is unnecessary for JavaScript resources" for all cases of script implanted into templates.

The reports can be found here:
- [About Page](documentation/validation/html-validator-about.png)
- [Vendor pages: add_product](documentation/validation/html-validator-add-product.png)
- [Catalog](documentation/validation/html-validator-catalog.png)
- [Contact Us](documentation/validation/html-validator-contacts.png)
- [Vendor pages: edit product](documentation/validation/html-validator-edit-product.png)
- [FAQ page](documentation/validation/html-validator-faq.png)
- [Home](documentation/validation/html-validator-home.png)
- [User Account pages: Orders](documentation/validation/html-validator-order-history.png)
- [User Account pages: Personal Info](documentation/validation/html-validator-personal_info.png)
- [Product Detail](documentation/validation/html-validator-product-detail.png)
- [User Account: shipping addresses](documentation/validation/html-validator-shipping-addr.png)
- [Vendor pages: dashboard](documentation/validation/html-validator-vendor-dashboard.png)
- [Vendor pages: orders](documentation/validation/html-validator-vendor-orders.png)
- [User Account pages: wishlist](documentation/validation/html-validator-wishlist.png)


### CSS Validation

- [CSS validation report: base.css](documentation/validation/css-valid-base.png)
- [CSS validation report: catalog.css](documentation/validation/css-valid-catalog.png)
- [CSS validation report: checkout.css](documentation/validation/css-valid-checkout.png)
- [CSS validation report: information.css](documentation/validation/css-valid-information.png.png)
- [CSS validation report: profile.css](documentation/validation/css-valid-profile.png)

__Explanation of Errors Revealed in Validator Results:__

All of the parse errors reported by W3C CSS validator are related to 'CSS nested rules', which the validator does not yet support, the 'nested CSS' syntax being a relatively new feature. The issue has been discussed in a number of places, particularly on GitHub issues , Reddit and some other less popular blogs.

It is acknowledged that such approach as CSS nesting reduces redundancy and simplifies the management of complex styles, leading to cleaner and more organized code. Additionally, CSS nesting aligns with the principles of modular design, which is especially in demand for complex and large-scale projects.
Moreover, CSS nesting is supported by all major modern browsers: 

| Browser Name: | Full support from: | Version released in: |
| ---- | ---- | ---- |
| Chrome | version 120 | released in 2023 |
| Edge | version 120 | released in 2023 |
| Firefox | version 117 | released in 2023 |
| Safari | version 17.2 | released in 2023 |
| Opera | version 106 | released in 2023 |
| Chrome for Android | version 125 | released in 2024 |
| Safari on iOS | version 17.2 | released in 2023 |
| Samsung Internet | version 25 | released in 2024 |
| Opera Mobile | version 80 | released in 2023 |
| Firefox for Android | version 126 | released in 2024 |

[Link to 'Can I Use' reg Nesting Selector](https://caniuse.com/mdn-css_selectors_nesting)

[Using CSS Nesting Selector MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting/Using_CSS_nesting)

### PEP 8
I used Flake8 package for checking the custom project folders for Python compliance in CLI.
- [Pep8: carols_home app](documentation/validation/flake8/flake-carols-home.png)

'F401 imported but unused': 

'django.contrib.admin' in admin.py \
'django.db.models' in models.py\
'django.test.TestCase' in tests.py

The above files are empty except standard imports pre-filled by django when starting application.\
I deliberately left them unscathed to utilize these files in further development.

- [Pep8: carols_project folder](documentation/validation/flake8/flake-carols-project.png)

E501 line too long found in my settings.py, particularly for the following:
~~~
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
~~~

I leave it as is because if I break it it will become quite less readable.

F811 'redefinition of unused 'handler404' from line1': 


font-optical-sizing: auto
https://webreference.com/css/properties/font-optical-sizing/

~~~
<script>
    streetAddress = "{{ shipping_details.street_address }}";
    townCity = "{{ shipping_details.town_city }}";
    county = "{{ shipping_details.county }}";
    postcode = "{{ shipping_details.postcode }}";
    country = "{{ shipping_details.country }}";
    phoneNumber = "{{ shipping_details.phone_number }}";
    fullName = "{{ shipping_details.first_name }} {{ shipping_details.last_name }}";
    billingName = "{{ billing_details.billing_name }}";
    billingEmail = "{{ billing_details.billing_email }}";
    billingPhone = "{{ billing_details.billing_phone_number }}";
</script>
~~~

// Service Provider Signup
$('#service-provider-signup').submit(function(event) {
    event.preventDefault();
    var email = $('#email').val();
    var username = $('#username').val();
    var phone = $('#phone').val();
    var city = $('#city').val();
    var password = $('#password').val();
    var otp = $('#otp').val();

    $.ajax({
        url: '/service_provider/signup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({email, username, phone, city, password, otp}),
        success: function(response) {
            $('#response').html('<div class="alert alert-success">' + response.message + '</div>');
        },
        error: function(error) {
            $('#response').html('<div class="alert alert-danger">' + error.responseJSON.error + '</div>');
        }
    });
});

// Customer Signup
$('#customer-signup').submit(function(event) {
    event.preventDefault();
    var email = $('#email').val();
    var username = $('#username').val();
    var password = $('#password').val();
    var otp = $('#otp').val();

    $.ajax({
        url: '/customer/signup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({email, username, password, otp}),
        success: function(response) {
            $('#response').html('<div class="alert alert-success">' + response.message + '</div>');
        },
        error: function(error) {
            $('#response').html('<div class="alert alert-danger">' + error.responseJSON.error + '</div>');
        }
    });
});

// Search Service Providers
$('#search-service').submit(function(event) {
    event.preventDefault();
    var city = $('#city').val();
    var date = $('#date').val();

    $.ajax({
        url: '/customer/search_service_providers',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({city, date}),
        success: function(response) {
            var html = '<ul>';
            response.available_providers.forEach(function(provider) {
                html += `<li>${provider[1]} (${provider[0]})</li>`;
            });
            html += '</ul>';
            $('#results').html(html);
        },
        error: function(error) {
            $('#results').html('<div class="alert alert-danger">No providers found.</div>');
        }
    });
});

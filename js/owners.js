

/*global BBS _config*/

var BBS = window.BBS || {};
BBS.map = BBS.map || {};

(function entryScopeWrapper($) {
    var authToken;
    BBS.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = '/signin.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = '/signin.html';
    });
    function insertRecord(record) {
        $.ajax({
            method: 'POST',
            url: _config.api.invokeUrl + '/owner',
            headers: {
                Authorization: authToken
            },
            data: JSON.stringify({
                Item: {
                  Name: record[0].value,
                  Address: record[1].value,
                  PhoneNumber: record[2].value
                }
            }),
            contentType: 'application/json',
            success: completeRequest,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error submitting: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured when trying to record:\n' + jqXHR.responseText);
            }
        });
    }

    function completeRequest(result) {
        console.log('Response received from API: ', result);
    }

    // Register click handler for #request button
    $(function onDocReady() {
        $('#request').click(handleRequestClick);
        $(BBS.map).on('pickupChange', handlePickupChanged);

        BBS.authToken.then(function updateAuthMessage(token) {
            if (token) {
                displayUpdate('You are authenticated. Click to see your <a href="#authTokenModal" data-toggle="modal">auth token</a>.');
                $('.authToken').text(token);
            }
        });

        if (!_config.api.invokeUrl) {
            $('#noApiMessage').show();
        }
    });

    function handlePickupChanged() {
        var requestButton = $('#request');
        requestButton.text('Request Unicorn');
        requestButton.prop('disabled', false);
    }

    function handleRequestClick(event) {
        var pickupLocation = BBS.map.selectedPoint;
        event.preventDefault();
        requestUnicorn(pickupLocation);
    }
    $("#my_form").submit(function(e) {
      e.preventDefault();
      console.log($('#my_form').serializeArray());
      insertRecord($('#my_form').serializeArray());

    });


    function displayUpdate(text) {
        $('#updates').append($('<li>' + text + '</li>'));
    }
}(jQuery));



/*global BBS _config*/

var BBS = window.BBS || {};
BBS.map = BBS.map || {};

(function entryScopeWrapper($) {
    var authToken;
    BBS.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
            console.log(authToken)
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
            url: _config.api.invokeUrl + '/rds',
            headers: {
                Authorization: authToken
            },
            data: JSON.stringify({
                record: {
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
        $("#my_form").submit(handleRequestClick);
        $(BBS.map).on('pickupChange', handlePickupChanged);

        BBS.authToken.then(function updateAuthMessage(token) {
            if (token) {
                displayUpdate('You are authenticated. Click to see your <a href="#authTokenModal" data-toggle="modal">auth token</a>.');
                $('.authToken').text(token);
            }
        });

        if (!_config.api.invokeUrl) {
            console.log("no api");
        }
    });

    function handlePickupChanged() {
        var requestButton = $('#request');
        requestButton.text('Request Unicorn');
        requestButton.prop('disabled', false);
    }

    function handleRequestClick(event) {
        event.preventDefault();
        console.log($('#my_form').serializeArray());
        insertRecord($('#my_form').serializeArray());
    }



    function displayUpdate(text) {
        console.log(text);
    }
}(jQuery));

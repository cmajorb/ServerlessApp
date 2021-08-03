
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log(cookieValue);
    return cookieValue;
}

jQuery(function ($) {

    var $upload = $('#fileSubmit');
    const csrftoken = getCookie('csrftoken');
    
    $upload.on('submit', function (e) {
        e.preventDefault();
        const fileSelect = document.getElementById("customFile").files[0];
        fileName = encodeURI(fileSelect.name);

        $.ajax({
            url: baseurl + "/upload/" + fileName,
            type: 'PUT',
            processData: false,
            contentType: false,
            data: fileSelect,
            headers: {
                "X-CSRFToken": csrftoken
            },
            
            success: function (result) {
                console.log(result)
                console.log("success");
            }
        });

    });

});


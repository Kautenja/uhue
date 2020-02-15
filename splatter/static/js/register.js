
function register_hue() {
    $('#register_button').hide();
    $('#register_loader').show();
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/hue/register",
        data: JSON.stringify({}),
        success: function (data) {
            if ("PhueRegistrationException" in data) {
                $('#register_loader').hide();
                $('#register_button').show();
                alert('The bridge button has not been pressed in 30 seconds!');
            }
        },
        dataType: "json"
    });

}

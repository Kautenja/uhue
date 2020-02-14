
/**
    Set a value for a light on the hue server.

    @param light_id the ID for the light to set
    @param parameter the name of the parameter to set
    @param value the value to set the parameter to

*/
function set_light(light_id, parameter, value) {
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/lights",
        data: JSON.stringify({
            "light_id": light_id,
            "parameter": parameter,
            "value": value
        }),
        success: function (data) {
            console.log("TODO: giggity");
        },
        dataType: "json"
    });
}

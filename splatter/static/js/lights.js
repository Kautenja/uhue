
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

/**
    Set a color value for a light on the hue server.

    @param light_id the ID for the light to set
    @param value the value to set the color to

*/
function set_color(light_id, value) {
    set_light(light_id, 'color', String(value));
}

/**
    Set a the on state for a light on the hue server.

    @param light_id the ID for the light to set
    @param checkbox the check-box to determine the on state from

*/
function set_on(light_id, checkbox) {
    set_light(light_id, 'on', $(checkbox).is(":checked"));
}

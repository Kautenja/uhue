/**
    The API for the Hue server.
*/

// ---------------------------------------------------------------------------
// MARK: Registration / Status
// ---------------------------------------------------------------------------

/**
    Send a request to register the server with the hue bridge.
*/
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

// ---------------------------------------------------------------------------
// MARK: Lights
// ---------------------------------------------------------------------------

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
        url: "/hue/lights",
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
function set_light_color(light_id, value) {
    set_light(light_id, 'color', String(value));
}

/**
    Set a the on state for a light on the hue server.

    @param light_id the ID for the light to set
    @param checkbox the check-box to determine the on state from

*/
function set_light_on(light_id, checkbox) {
    set_light(light_id, 'on', $(checkbox).is(":checked"));
}

// ---------------------------------------------------------------------------
// MARK: Groups
// ---------------------------------------------------------------------------

/**
    Set a value for a group on the hue server.

    @param group_id the ID for the group to set
    @param parameter the name of the parameter to set
    @param value the value to set the parameter to

*/
function set_group(group_id, parameter, value) {
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/hue/groups",
        data: JSON.stringify({
            "group_id": group_id,
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
    Set a color value for a group on the hue server.

    @param group_id the ID for the group to set
    @param value the value to set the color to

*/
function set_group_color(group_id, value) {
    set_group(group_id, 'color', String(value));
}

/**
    Set a the on state for a group on the hue server.

    @param group_id the ID for the group to set
    @param checkbox the check-box to determine the on state from

*/
function set_group_on(group_id, checkbox) {
    set_group(group_id, 'on', $(checkbox).is(":checked"));
}

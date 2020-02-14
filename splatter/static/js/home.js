
// function set_brightness(light_id, value) {
//     $.ajax({
//         type: "POST",
//         contentType: "application/json; charset=utf-8",
//         url: "/lights",
//         data: JSON.stringify({
//             "light_id": light_id,
//             "function": "bri",
//             "value": value
//         }),
//         success: function (data) {
//             console.log("TODO: giggity");
//         },
//         dataType: "json"
//     });
// }

function set_hue_value(light_id, parameter, value) {
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

function set_brightness(light_id, value) {
    set_hue_value(light_id, "bri", value);
}


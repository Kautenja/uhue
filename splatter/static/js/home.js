
function set_brightness(light_id, value) {
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/lights",
        data: JSON.stringify({
            "light_id": light_id,
            "function": "bri",
            "value": value
        }),
        success: function (data) {
            console.log(data.light_id);
        },
        dataType: "json"
    });
}

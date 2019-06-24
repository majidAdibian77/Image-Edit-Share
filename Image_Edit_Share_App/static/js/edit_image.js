function post_button() {

    $.ajax({
        type: "GET",
        url: '/set_post_text',
        data: {
            "post_text": $('#post_text').val(),
            "post_pk": $('#post_text').attr('name'),
            "image_url": $('#show_image').attr('src'),
        },
        dataType: "json",
        success: function (data) {
            alert("Posting image is successful!");
        },
        failure: function (data) {
            alert('There is a problem!!!');
        }
    });
}

function change_black_white() {
    $.ajax({
        type: "GET",
        url: '/change_black_white',
        data: {
            "general_image_url": $('#show_image').attr('name'),
            "new_image_url": $('#show_image').attr('src')
        },
        dataType: "json",
        success: function (data) {
            $("#show_image").attr("src", data["newImage_url"]);
        },
        failure: function (data) {
            alert('There is a problem!!!');
        }
    });
}

function reset_image() {
    var general_url_image = $('#show_image').attr('name');
    var new_url_image = $('#show_image').attr('src');

    if (general_url_image != new_url_image) {
        $.ajax({
            type: "GET",
            url: '/reset_image',
            data: {
                "image_url": new_url_image
            },
            dataType: "json",
            success: function (data) {
                $("#show_image").attr("src", data["newImage_url"]);
                $("#show_image").attr("width", data["width"]);
                $("#show_image").attr("height", data["height"]);
            },
            failure: function (data) {
                alert('There is a problem!!!');
            }
        });
    }
}

function change_size() {
    var width_image = $('#width_image');
    var height_image = $('#height_image');
    var width = width_image.val();
    var height = height_image.val();
    if (width < 200) {
        width_image.css('background', 'red');
        width_image.val(200);
        width = 200;
    }
    else if (width > 500) {
        width_image.css('background', 'red');
        width_image.val(400);
        width = 400;
    }
    if (height < 300) {
        height_image.css('background', 'red');
        height_image.val(300);
        height = 300;
    }
    else if (height > 600) {
        height_image.css('background', 'red');
        height_image.val(500);
        height = 500;
    }
    $.ajax({
        type: "GET",
        url: '/change_size_of_image',
        data: {
            "image_url": $('#show_image').attr('name'),
            "width": width,
            "height": height,
        },
        dataType: "json",
        success: function (data) {
            $("#show_image").attr("src", data["newImage_url"]);
            $('#show_image').attr('width', width);
            $('#show_image').attr('height', height);
        },
        failure: function (data) {
            alert('There is a problem!!!');
        }
    });
}

function change_contract() {
    $.ajax({
        type: "GET",
        url: '/change_contract_image',
        data: {
            "image_url": $('#show_image').attr('name'),
            "factor": $('#contract_range').val(),
        },
        dataType: "json",
        success: function (data) {
            alert(data["newImage_url"]);
            $("#show_image").attr("src", data["newImage_url"]);
        },
        failure: function (data) {
            alert('There is a problem!!!');
        }
    });
}

function download() {
    $("#download-link").attr("href", $("#show_image").attr("src"))
}
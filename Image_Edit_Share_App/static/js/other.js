function add_score_image(post_pk) {
    $.ajax({
        type: "GET",
        url: '/add_score_image',
        data: {
            "post_pk": post_pk
        },
        dataType: "json",
        success: function (data) {
            if (data["test"]) {
                $('#show-score-'+post_pk).text("score:"+data["new_score"]);
                alert("Your score is added!");
            }
            else {
                alert("You can not!!");
            }
        },
        failure: function (data) {
            alert('There is a problem!!!');
        }
    });
}
function user_not_register() {
    alert("You should register or log in at first!")
}


function add_comment_button(postPk) {
    $.ajax({
        type: "GET",
        url: '/user_add_comment',
        data: {
            "comment_text": $('#user-comment-' + postPk).val(),
            "post_pk": postPk,
        },
        dataType: "json",
        success: function (data) {
            location.href = data["url"];
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}


function approve_comment(comment_pk) {
    $.ajax({
        type: "GET",
        url: '/approve_comment',
        data: {
            "comment_pk": comment_pk,
            // "user_pk": $('#approve-comment-' + comment_pk).attr("name")
        },
        dataType: "json",
        success: function (data) {
            location.href = data["url"];
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}

function delete_comment(comment_pk) {
    $.ajax({
        type: "GET",
        url: '/delete_comment',
        data: {
            "comment_pk": comment_pk,
            // "user_pk": $('#approve-comment-' + comment_pk).attr("name")
        },
        dataType: "json",
        success: function (data) {
            location.href = data["url"];
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}

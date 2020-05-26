

$("#frmbtn").on("click", function(event) {
        user_edit();
});

function user_edit() {
    // initiate variables with form content
    var email = $("#inputEmail").val();
    var firstname = $("#inputName").val();
    var lastname = $("#inputName2").val();
    var company = $("#inputCompany").val();

    var action = function(d) {
        window.location.replace("/dashboard/account")
    }

    $.ajax({
        type: "PUT",
        url: "/rest-auth/user/",
        data: "email=" + email + "&firstname=" + firstname + "&lastname=" + lastname + "&company=" + company,
        success: action,
        error: action,
    });
};


$("#passbtn").on("click", function(event) {
    new_pass();
});

function new_pass() {
    // initiate variables with form content
    var password = $("#inputpass").val();

    var action = function(d) {
        $("#error_pass").html(" ")
        window.location.replace("/dashboard/account")
    }
    var action2 = function(d) {
        $("#error_pass").html("Password must contain at least 8 characters and not entirely numeric!")
    }
    $.ajax({
        type: "POST",
        url: "/rest-auth/password/change/",
        data: "new_password1=" + password + "&new_password2=" + password,
        success: action,
        error: action2,
    });
};




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


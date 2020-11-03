
function onClickEyeIcon() {
    var password = document.getElementById("password");
    var eyebox = document.getElementById("eye-box");

    if (password.type == "password") {
        password.type = "text";
        eyebox.style.opacity = 0;
    } else {
        password.type = "password";
        eyebox.style.opacity = 100;
    }
}

function forgotPass() {
    alert("Forgot password!!!");
}
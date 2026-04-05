$(document).ready(function () {
  $("#show-register").click(function () {
    $("#register-form").addClass("active");
    $("#login-form").removeClass("active");
  });

  $("#show-login").click(function () {
    $("#login-form").addClass("active");
    $("#register-form").removeClass("active");
  });

  $("#register-form").submit(function (e) {
    e.preventDefault();
    $.ajax({
      url: "/api/register",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        name: $("#reg-name").val(),
        email: $("#reg-email").val(),
        password: $("#reg-password").val()
      }),
      success: function (response) {
        alert(response.message);
      },
      error: function (xhr) {
        alert(xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'Đăng ký không thành công');
      }
    });
  });

  $("#login-form").submit(function (e) {
    e.preventDefault();
    $.ajax({
      url: "/api/signin",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        email: $("#login-email").val(),
        password: $("#login-password").val()
      }),
      success: function (response) {
        alert(response.message);
        window.location.href = "/tasks";
      },
      error: function (xhr) {
        alert(xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'Đăng nhập không thành công');
      }
    });
  });
});
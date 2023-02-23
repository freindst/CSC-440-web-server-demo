window.addEventListener('DOMContentLoaded', (event) => {
    $.ajax({
        url: "/api/login"
      }).done(function(data) {
        console.log(data);
      });
});
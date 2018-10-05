$(document).ready(function() {
  // add comment form submission
  $("#addComment").click(function() {
    $.post({
      url: $("form#comment").data("action"),
      data: $("form#comment").serialize(),
      success: function(data) {
        content =
          data.vote > 0 ? "&plus;" : data.vote == 0 ? "&times;" : "&minus;";

        $("#newComment").before(
          '<tr><th scope="row">' +
            data.game +
            "</th>" +
            "<td>" +
            data.comment +
            '</td><td class="text-center">' +
            content +
            "</td>" +
            "<td>" +
            data.date +
            "</td></tr>"
        );
        $(".typeahead#game").typeahead("val", "");
      }
    }).fail(function(data) {
      alert(data.responseJSON.error);
    });
  });

  $("#clearNewUser").click(function() {
    $("#newUserForm").trigger("reset");
  });

  $("#submitNewUser").click(function() {
    $.post({
      url: $("form#newUserForm").data("action"),
      data: $("#newUserForm").serialize(),
      success: function(data) {
        $("#newUser").before(
          '<tr><th scope="row"><a href="/adm/user/' +
            data.username +
            '">' +
            data.username +
            "</a></td><td></td></tr>"
        );
      }
    }).fail(function(data) {
      alert(data.responseJSON.error);
    });
  });
});
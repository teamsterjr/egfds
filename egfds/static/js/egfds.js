$(document).ready(function() {
  // game typeahead
  $(".typeahead#game")
    .typeahead(null, {
      display: "name",
      source: new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace("name"),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
          url: "/games/games.json",
          cache: false
        }
      }),
      hint: false,
      highlight: true
    })
    .on("typeahead:selected", function(e, datum) {
      $(this).data("found", datum);
    })
    .on("typeahead:autocomplete", function(e, datum) {
      $(this).data("found", datum);
    })
    .on("change", function(event, datum) {
      if ($(this).data("found")) {
        $("#instanceId").val($(this).data("found").instance_id);
      } else {
        // also show the genre drop down
        $("#instanceId").val("");
      }
      jQuery.removeData(this, "found");
    });

  // add comment form submission
  $("#addComment").click(function() {
    $.post({
      url: $("form#comment").data("action"),
      data: $("form#comment").serialize(),
      success: function(data) {
        image =
          data.vote > 0
            ? "thumb-up.svg"
            : data.vote == 0
              ? "meh.svg"
              : "thumb-down.svg";

        $("#newComment").before(
          '<tr><th scope="row">' +
            data.game +
            "</th>" +
            "<td>" +
            data.comment +
            '</td><td class="text-center"><img class="icon" src="/static/images/' +
            image +
            '"></td>' +
            "<td>" +
            data.date +
            "</td></tr>"
        );
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
        console.log(data);
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
  /*
  $("#deleteUser").click(function () {
      $.post({
          url: '{{url_for('admin.add_user')}}',
          data: $('#newUserForm').serialize(),
          success: function (data) {

          }
      })
  })
  */

  var table = $("#recommendation").DataTable({
    info: false,
    paging: false,
    order: ["2", "desc"],
    columnDefs: [
      {
        visible: false,
        targets: [3, 4, 5, 6]
      }
    ],
    columns: [
      {
        name: "name"
      },
      {
        name: "genre"
      },
      {
        name: "score"
      },
      {
        name: "votes"
      },
      {
        name: "up"
      },
      {
        name: "down"
      },
      {
        name: "type"
      }
    ],
    searching: false
  });

  $("#gameModal").on("show.bs.modal", function(event) {
    var button = $(event.relatedTarget);
    instanceId = button.data("instanceid");
    comments_table = $(".comments-table");
    $.get({
      url: "/games/" + instanceId + "/comments.json",
      success: function(data) {
        comments_table.empty();
        data.forEach(function(element) {
          console.log(element);
          $("<dl/>", {class:"row"})
            .append(
              $("<dd/>", {class:'col-sm-3'}).append(
                $("<p/>", { text: element.username, class: "text-primary" }),
                $("<p/>").html($("<small/>", { text: element.date }))
              ),
              $("<dd/>", {
                // split and add ps
                class:'col-sm-9',
                html: element.comment.replace(/(?:\r\n|\r|\n){2,}/g, '<br>')
              })
            )
            .appendTo(comments_table);
        });
      }
    });

    var modal = $(this);
    var data = table.row(button).data();
    modal.find(".modal-title").text(data[0]);
    modal.find(".up-vote").html("&plus; " + data[4]);
    modal.find(".no-vote").html("&minus; " + (data[3] - data[4] - data[5]));
    modal.find(".down-vote").html("&times; " + data[5]);
  });
});

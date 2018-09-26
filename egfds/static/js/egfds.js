$(document).ready(function() {
  // datastore for games
  var games = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace("name"),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: {
      url: "/games/games.json",
      cache: false,
      transform: function(data) {
        return data.data
      }
    }
  });

  // game typeahead
  $(".typeahead#game")
    .typeahead(null, {
      display: "name",
      source: games,
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
        $(".typeahead#game").typeahead("val", "");
      }
      jQuery.removeData(this, "found");
    });

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


  $("#gameModal").on("show.bs.modal", function(event) {
    var button = $(event.relatedTarget);
    var data = table.row(button.parents('tr')).data();
    instanceId = data.instance_id
    comments_table = $(".comments-table");
    comments_table.empty();
    var modal = $(this);
    modal.find(".modal-title").text(button.text())
    modal.find(".up-vote").html("&plus; " + data.up)
    modal.find(".no-vote").html("&times; " + (data.num_votes - data.total))
    modal.find(".down-vote").html("&minus; " + data.down)
    if(! data.num_comments) {
      comments_table.text('No comments yet')
      return;
    }

    $.get({
      url: "/games/" + instanceId + "/comments.json",
      success: function(data) {
        data.forEach(function(element) {
          $("<dl/>", { class: "row" })
            .append(
              $("<dd/>", { class: "col-sm-2" }).append(
                $("<p/>", { text: element.username, class: "text-primary" }),
                $("<p/>").html($("<small/>", { text: element.date }))
              ),
              $("<dd/>", {
                class: "col-sm-1",
                html:
                  element.vote > 0
                    ? "&plus;"
                    : element.vote
                      ? "&minus;"
                      : "&times;"
              }),
              $("<dd/>", {
                //TODO split and add p's
                class: "col-sm-9",
                html: element.comment.replace(/(?:\r\n|\r|\n){2,}/g, "<br>")
              })
            )
            .appendTo(comments_table);
        });
      }
    });

  });
});

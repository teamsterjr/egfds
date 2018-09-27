var table;
$(document).ready(function() {
  $(function() {});

  table = $("#recommendation")
    .DataTable({
      deferRender: true,
      //rowGroup: { dataSrc: "interest" },
      //orderFixed: [3, 'desc'],
      columns: [
        {
          name: "Title",
          data: "name",
          render: function(data, type, row) {
            return (
              '<a href="#" data-instance_id="' +
              row.instance_id +
              '" data-toggle="modal" data-target="#gameModal">' +
              data +
              "</a>"
            );
          }
        },
        {
          name: "Genre",
          data: "genre"
        },
        {
          name: "Score",
          data: "total",

          render: function(data, type, row) {
            votes =
              "&plus;" +
              row.up +
              " &times;" +
              (row.num_votes - row.total) +
              " &minus;" +
              row.down +
              " #" +
              row.num_votes;

            button = $('<div/>').append(
              $('div', {
                class:"blah",
                html:'hello'
              })
            )

            console.log(button.html())
            return (
              '<button type="button" data-trigger="focus" class="btn btn-link" data-toggle="popover" data-html="true" data-placement="bottom" data-content="' +
              votes +
              '">' +
              data +
              "</button>"
            );
            // move to generated from jquery
          }
        },
        {
          name: "interest",
          visible: false,
          data: 'interest'
        }
      ],
      info: false,
      paging: false,
      order: [[2, "desc"]],
      statesave: false,
      searching: false,
      ajax: {
        url: "/games/games.json",
        dataSrc: function(json) {
          for (var i = 0, ien = json.data.length; i < ien; i++) {
            if (json.data[i].total > 0) {
              interest = "Yay!";
            } else if (json.data[i].total < 0) {
              interest = "Boo!";
            } else {
              interest = "Meh";
            }
            json.data[i]["interest"] = interest;
          }
          return json.data;
        }
      }
    })
    .on("draw.dr", function() {
      $('[data-toggle="popover"]').popover();
    })
});

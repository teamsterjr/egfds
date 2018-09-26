var table;
$(document).ready(function() {
    table = $("#recommendation").DataTable({
    "deferRender": true,
    "columns": [
      {
        name: "Title",
        data: "name",
            "render": function ( data, type, row ) {
            return '<a href="#" data-instance_id="'+row.instance_id+'" data-toggle="modal" data-target="#gameModal">' + data + '</a>'
            }

      },
      { name: "Genre", data: "genre"


    },
      { name: "Score", data: "total" },
      { name: "Votes", data: "num_votes", visible:false },
      { name: "Comments", data: "num_comments", visible:true },
      { name: "Up Votes", data: "up", visible:false },
      { name: "Down Votes", data: "down", visible:false }
    ],
    info: false,
    paging: false,
    order: [[2, "desc"]],
    searching: false,
    ajax: {url:"/games/games.json"}
  })
});
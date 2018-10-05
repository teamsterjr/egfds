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


  $("#gameModal").on("show.bs.modal", function(event) {
    var button = $(event.relatedTarget);
    var data = table.row(button.parents('tr')).data();
    instanceId = data.instance_id
    contentDiv = $(this).find('.modal-content')

    $.get({
      url: "/games/" + instanceId + "/",
      success: function(data) {
        contentDiv.html(data)
        addCollapse()
      }
    });

  });
  addCollapse()

});

function addCollapse() {
  $(".videoCollapse").on("show.bs.collapse", function(event) {
    data=$(this).parent().find('a#'+$(this).attr('aria-labelledby'))
    videoSRC = data.data( "video" )
    videoLink = data.data( "link" )
    iframe = $(this).find('iframe.videoFrame')
    link = $(this).find('a.videoLink')
    link.attr('href', videoLink)
    link.text(videoLink)
    iframe.attr('src', videoSRC)
  })

  $(".videoCollapse").on("hiden.bs.collapse", function(event) {
    $(this).find('iframe').removeAttr('src')
  });
}
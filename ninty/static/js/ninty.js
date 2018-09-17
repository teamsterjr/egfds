    $(document).ready(function () {
      // game typeahead
      $('.typeahead#game').typeahead(null, {
          display: 'name',
          source: new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            prefetch: {
              url: '/games/games.json',
              cache: false
            }
          }),
          hint: false,
          highlight: true
        }).on('typeahead:selected', function (e, datum) {
          $(this).data('found', datum)
        }).on('typeahead:autocomplete', function (e, datum) {
          $(this).data('found', datum)
        })
        .on('change', function (event, datum) {
          if ($(this).data('found')) {
            $('#instanceId').val($(this).data('found').instance_id)
          } else {
            // also show the genre drop down
            $('#instanceId').val("")
          }
          jQuery.removeData(this, 'found')
        });

      // add comment form submission
      $('#addComment').click(function () {
        $.post({
          url: $('form#comment').data('action'),
          data: $('form#comment').serialize(),
          success: function (data) {
            image = (
                data.vote > 0 ? "thumb-up.svg" :
                data.vote ==0 ? "meh.svg" :
                "thumb-down.svg"
            )

            $("#newComment").before('<tr><th scope="row">' + data.game + '</th>' +
            '<td>' + data.comment +
            '</td><td class="text-center"><img class="icon" src="/static/images/' + image + '"></td>' +
            '<td>' + data.date + '</td></tr>')
          }
        }).fail(function (data) {
          alert(data.responseJSON.error)
        })
      })

      $("#clearNewUser").click(function () {
        $('#newUserForm').trigger("reset");
      })

      $("#submitNewUser").click(function () {
        $.post({
          url: $('form#newUserForm').data('action'),
          data: $('#newUserForm').serialize(),
          success: function (data) {
            console.log(data)
            $("#newUser").before('<tr><th scope="row"><a href="/adm/user/' + data.username + '">' + data.username + '</a></td><td></td></tr>')
          },
        }).fail(function (data) {
          alert(data.responseJSON.error)
        })
      })
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

      $('#recommendation').DataTable({
        info: false,
        paging: false,
        order: ['2', 'desc'],
        columnDefs: [{
          "visible": false,
          "targets": [3, 4, 5, 6]
        }],
        searching: false
      });

      $('#exampleModalLong').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget).closest('tr')
        console.log(button.data())
      });
    });
$(document).ready(function () {
    $('#searchFormFindGame').on('submit', function (e) {
        e.preventDefault();

        $.ajax({
            // Access the URL from the data attribute
            url: $(this).data('url'),
            data: $(this).serialize(),
            success: function (data) {
                var searchGamesForMainThread = $('#searchGamesForMainThread');
                searchGamesForMainThread.empty();

                $.each(data, function (i, game) {
                    var listItem = $('<li>').addClass('result-item');
                    if (i === 0) {
                        listItem.addClass('first-result-item');
                    }

                    var form = $('<form>').attr('method', 'post').attr('action', $('#searchFormFindGame').data('base-action-url') + game.id + '/');
                    form.append($('<input>').attr('type', 'hidden').attr('name', 'csrfmiddlewaretoken').val(getCookie('csrftoken')));
                    form.append($('<input>').attr('type', 'hidden').attr('name', 'game_name').val(game.name));
                    form.append($('<button>').addClass('result-button btn btn-primary w-100').text('Create Main Thread ' + game.name));

                    listItem.append(form);
                    searchGamesForMainThread.append(listItem);
                });

                // Handle form submission via AJAX
                searchGamesForMainThread.on('submit', 'form', function (e) {
                    e.preventDefault();

                    $.ajax({
                        url: $(this).attr('action'),
                        type: 'POST',
                        data: $(this).serialize(),
                        beforeSend: function (xhr) {
                            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                        },
                        success: function (data) {
                            // Handle success
                        },
                        error: function (xhr, status, error) {
                            // Handle error
                        }
                    });
                });
            }
        });
    });

    $('#searchFormMainThread').on('submit', function (e) {
        e.preventDefault();

        $.ajax({
            // Access the URL from the data attribute
            url: $(this).data('url'),
            data: $(this).serialize(),
            success: function (data) {
                var searchCreatedMainThreads = $('#searchCreatedMainThreads');
                searchCreatedMainThreads.empty();

                $.each(data, function (i, thread) {
                    searchCreatedMainThreads.append('<p>' + thread.name + '</p>');
                });
            }
        });
    });
});
$(document).ready(function () {
    $('#searchFormFindGame').on('submit', function (e) {
        e.preventDefault();

        $.ajax({
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

                    var form = $('<form>').addClass('create-thread-form').attr('method', 'post').attr('action', $('#searchFormFindGame').data('base-action-url') + game.id + '/');
                    form.append($('<input>').attr('type', 'hidden').attr('name', 'csrfmiddlewaretoken').val(getCookie('csrftoken')));
                    form.append($('<input>').attr('type', 'hidden').attr('name', 'game_name').val(game.name));
                    form.append($('<button>').addClass('result-button btn btn-primary w-100').text('Create Main Thread ' + game.name));

                    listItem.append(form);
                    searchGamesForMainThread.append(listItem);
                });
            }
        });
    });

    $('#searchFormMainThread').on('submit', function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).data('url'),
            data: $(this).serialize(),
            success: function (data) {
                var searchCreatedMainThreads = $('#searchCreatedMainThreads');
                searchCreatedMainThreads.empty();

                $.each(data, function (i, thread) {
                    var accordionItem = $('<div>').addClass('accordion-item mb-3');

                    var accordionHeader = $('<h2>').addClass('accordion-header').attr('id', 'heading' + i);
                    var accordionButton = $('<button>').addClass('accordion-button collapsed').attr('type', 'button')
                        .attr('data-bs-toggle', 'collapse').attr('data-bs-target', '#collapse' + i)
                        .attr('aria-expanded', 'false').attr('aria-controls', 'collapse' + i)
                        .text(thread.name);
                    accordionHeader.append(accordionButton);

                    var accordionCollapse = $('<div>').attr('id', 'collapse' + i).addClass('accordion-collapse collapse')
                        .attr('aria-labelledby', 'heading' + i).attr('data-bs-parent', '#searchCreatedMainThreads');
                    var accordionBody = $('<div>').addClass('accordion-body').text(thread.content);
                    var deleteButton = $('<button>').addClass('delete-button btn delete-button w-100').text('Delete Main Thread')
                        .attr('data-thread-id', thread.id);
                    accordionBody.append(deleteButton);
                    accordionCollapse.append(accordionBody);

                    accordionItem.append(accordionHeader).append(accordionCollapse);
                    searchCreatedMainThreads.append(accordionItem);
                });
            }
        });
    });

    $(document).on('click', '.delete-button', function () {
        var threadId = $(this).data('thread-id');
        var button = $(this);  // Store the clicked button in a variable

        $('#deleteModal').modal('show');  // Show the modal

        $('#confirmDelete').on('click', function () {
            $.ajax({
                url: '/delete_a_main_thread/',
                method: 'POST',
                data: {
                    'thread_id': threadId,
                    'csrfmiddlewaretoken': getCookie('csrftoken')
                },
                success: function () {
                    button.closest('.accordion-item').remove();  // Remove the thread from the page
                    $('#deleteModal').modal('hide');  // Hide the modal
                }
            });
        });
    });
});
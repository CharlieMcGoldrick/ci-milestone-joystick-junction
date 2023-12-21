$(document).ready(function () {
    $('#searchForm').on('submit', function (e) {
        e.preventDefault();
        var url = $(this).data('url');  // Get the URL from the data attribute
        $.ajax({
            url: url,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                var threadList = $('#threadList');
                threadList.empty();
                $.each(data, function (index, thread) {
                    threadList.append('<p>' + thread.name + '</p>');
                });
            }
        });
    });
});
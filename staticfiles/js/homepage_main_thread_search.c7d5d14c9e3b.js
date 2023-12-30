$(document).ready(function () {
    $("#homepageSearchFormMainThread").on("submit", function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).data('url'),
            data: $(this).serialize(),
            success: function (data) {
                var resultsContainer = $("#homepageResultsContainer");
                resultsContainer.empty();

                if (data.no_results) {
                    // Display a message if no results were found
                    var noResultsMessage = $("<p>")
                        .addClass("mt-3")
                        .text("No threads match your request");
                    resultsContainer.append(noResultsMessage);
                } else {
                    // Display the results
                    $.each(data.results, function (i, thread) {
                        var link = $("<a>")
                            .attr("href", thread.url)
                            .addClass("result-link");
                        var listItem = $("<li>")
                            .addClass("btn result-button result-item w-100")
                            .text(thread.name);
                        link.append(listItem);
                        if (i === 0) {
                            listItem.addClass("mt-3");
                        }
                        resultsContainer.append(link);
                    });
                }
            },
        });
    });
});
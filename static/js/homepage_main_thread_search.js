$(document).ready(function () {
  $("#homepageSearchFormMainThread").on("submit", function (e) {
    e.preventDefault();

    $.ajax({
      url: $(this).data("url"), // Use the URL from the data attribute
      data: $(this).serialize(),
      success: function (data) {
        var resultsContainer = $("#homepageResultsContainer");
        resultsContainer.empty();

        if (data.no_results) {
          // Display a message if no results were found
          resultsContainer.append("<p>No threads match your request</p>");
        } else {
          // Display the results
          $.each(data.results, function (i, thread) {
            var listItem = $("<li>").addClass("result-item");
            listItem.append(
              "<a href='{% url 'main_thread_detail' game_id=" +
                thread.game_id +
                " %}'>" +
                thread.name +
                "</a>"
            );
            resultsContainer.append(listItem);
          });
        }
      },
    });
  });
});

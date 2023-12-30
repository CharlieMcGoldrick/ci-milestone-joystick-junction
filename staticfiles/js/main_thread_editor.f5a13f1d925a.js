$(document).ready(function () {
    // When the search form is submitted
    $("#searchFormFindGame").on("submit", function (e) {
        e.preventDefault();

        var formData = $(this).serializeArray();

        // Send an AJAX request to the server
        $.ajax({
            url: $(this).data("url"),
            data: $(this).serialize(),
            success: function (data) {
                var searchGamesForMainThread = $("#searchGamesForMainThread");
                searchGamesForMainThread.empty();

                // For each game returned by the server
                $.each(data, function (i, game) {
                    var listItem = $("<li>").addClass("result-item");
                    if (i === 0) {
                        listItem.addClass("first-result-item");
                    }

                    // Create a form for creating a new thread for the game
                    var form = $("<form>")
                        .addClass("create-thread-form")
                        .attr("method", "post")
                        .attr(
                            "action",
                            $("#searchFormFindGame").data("base-action-url") + game.id + "/"
                        );
                    form.append(
                        $("<input>")
                            .attr("type", "hidden")
                            .attr("name", "csrfmiddlewaretoken")
                            .val(getCookie("csrftoken"))
                    );

                    // Add hidden inputs for each game attribute
                    if (game.name) {
                        form.append(
                            $("<input>")
                                .attr("type", "hidden")
                                .attr("name", "game_name")
                                .val(game.name)
                        );
                    }
                    if (game.genres) {
                        form.append(
                            $("<input>")
                                .attr("type", "hidden")
                                .attr("name", "genres")
                                .val(JSON.stringify(game.genres))
                        );
                    }
                    if (game.platforms) {
                        form.append(
                            $("<input>")
                                .attr("type", "hidden")
                                .attr("name", "platforms")
                                .val(JSON.stringify(game.platforms))
                        );
                    }
                    if (game.summary) {
                        form.append(
                            $("<input>")
                                .attr("type", "hidden")
                                .attr("name", "summary")
                                .val(game.summary)
                        );
                    }
                    if (game.involved_companies) {
                        form.append(
                            $("<input>")
                                .attr("type", "hidden")
                                .attr("name", "involved_companies")
                                .val(JSON.stringify(game.involved_companies))
                        );
                    }
                    if (game.game_engines) {
                        form.append(
                            $("<input>")
                                .attr("type", "hidden")
                                .attr("name", "game_engines")
                                .val(JSON.stringify(game.game_engines))
                        );
                    }
                    if (game.aggregated_rating) {
                        form.append(
                            $("<input>")
                                .attr("type", "hidden")
                                .attr("name", "aggregated_rating")
                                .val(game.aggregated_rating)
                        );
                    }

                    // Add a button to create a new thread for the game
                    form.append(
                        $("<button>")
                            .addClass("btn result-button w-100")
                            .text("Create Main Thread " + game.name)
                    );

                    listItem.append(form);
                    searchGamesForMainThread.append(listItem);
                });
            },
        });
    });

    // When a thread creation form is submitted
    $(document).on("submit", ".create-thread-form", function (e) {
        e.preventDefault();

        var formData = $(this).serializeArray();
        var jsonData = {};

        // Convert form data to JSON
        $.each(formData, function (i, field) {
            jsonData[field.name] = field.value;
        });

        // Send an AJAX request to the server to create a new thread
        $.ajax({
            url: $(this).attr("action"),
            type: "POST",
            data: JSON.stringify(jsonData),
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            },
            success: function (response) {
                toastBody.textContent = response.success;
                notificationToast.show();
            },
            error: function (response) {
                toastBody.textContent = response.responseJSON.error;
                notificationToast.show();
            },
        });
    });

    // When the form with id "searchFormMainThread" is submitted
    $("#searchFormMainThread").on("submit", function (e) {
        e.preventDefault();

        // Send an AJAX request to the server
        $.ajax({
            url: $(this).data("url"),
            data: $(this).serialize(),
            success: function (data) {
                var searchCreatedMainThreads = $("#searchCreatedMainThreads");
                searchCreatedMainThreads.empty();

                // For each thread returned by the server
                $.each(data, function (i, thread) {
                    var accordionItem = $("<div>")
                        .addClass("accordion-item mb-3")
                        .attr("id", "thread-" + thread.game_id);

                    // Create an accordion item for the thread
                    var accordionHeader = $("<h2>")
                        .addClass("accordion-header")
                        .attr("id", "heading" + i);

                    // Create an accordion button for the thread
                    var accordionButton = $("<button>")
                        .addClass("accordion-button collapsed")
                        .attr("type", "button")
                        .attr("data-bs-toggle", "collapse")
                        .attr("data-bs-target", "#collapse" + i)
                        .attr("aria-expanded", "false")
                        .attr("aria-controls", "collapse" + i)
                        .text(thread.name);
                    accordionHeader.append(accordionButton);

                    // Create an accordion collapse for the thread
                    var accordionCollapse = $("<div>")
                        .attr("id", "collapse" + i)
                        .addClass("accordion-collapse collapse")
                        .attr("aria-labelledby", "heading" + i)
                        .attr("data-bs-parent", "#searchCreatedMainThreads");
                    var accordionBody = $("<div>").addClass("accordion-body");

                    // Define the fields to display for the thread
                    var fields = [
                        "name",
                        "summary",
                        "genres",
                        "platforms",
                        "involved_companies",
                        "game_engines",
                        "aggregated_rating",
                    ];

                    // For each field
                    $.each(fields, function (j, field) {
                        // Create a row for the field
                        var infoRow = $("<div>").addClass("info-row row");

                        var formattedField = field
                            .replace(/_/g, " ")
                            .replace(/\b\w/g, function (l) {
                                return l.toUpperCase();
                            });

                        var titleCol = $("<div>")
                            .addClass("info-title col-md-4")
                            .text(formattedField);
                        var dataCol = $("<div>").addClass("info-data col-md-4");

                        if (thread[field] && thread[field] !== "[]") {
                            if (
                                [
                                    "genres",
                                    "platforms",
                                    "involved_companies",
                                    "game_engines",
                                ].includes(field)
                            ) {
                                var parsedData = JSON.parse(thread[field]);
                                var names = parsedData
                                    .map((item) => item.name || item.company.name)
                                    .join(", ");
                                dataCol.text(names);
                            } else if (field === "aggregated_rating") {
                                dataCol.text(Math.floor(thread[field])); // Round down the rating
                            } else {
                                dataCol.text(thread[field]);
                            }
                        } else {
                            dataCol.text("N/A");
                        }

                        var switchCol = $("<div>").addClass("info-toggle col-md-4 form-switch");
                        var switchInput = $("<input>")
                            .addClass("form-check-input")
                            .attr("type", "checkbox")
                            .attr("id", field + "Switch")
                            .attr("role", "switch");
                        var switchLabel = $("<label>")
                            .addClass("form-check-label")
                            .attr("for", field + "Switch");
                        switchCol.append(switchInput).append(switchLabel);

                        if (field === "name" || field === "summary") {
                            switchInput.attr("checked", true);
                        }

                        infoRow.append(titleCol).append(dataCol).append(switchCol);

                        if (field === "name" || field === "summary") {
                            switchInput.attr("disabled", true);
                            switchLabel.css("color", "#6c757d"); // Set the label color to grey
                        }

                        if (dataCol.text() !== "N/A") {
                            accordionBody.append(infoRow);
                        }
                    });

                    // Create a button to publish the thread
                    var publishButton = $("<button>")
                        .addClass("action-button btn publish-button w-100 w-md-50")
                        .text("Publish Main Thread")
                        .attr("data-game-id", thread.game_id);
                    accordionBody.append(publishButton);

                    // Create a button to unpublish the thread
                    var unpublishButton = $("<button>")
                        .addClass("action-button btn unpublish-button w-100 w-md-50")
                        .text("Unpublish Main Thread")
                        .attr("data-game-id", thread.game_id);
                    accordionBody.append(unpublishButton);

                    // Create a button to delete the thread
                    var deleteButton = $("<button>")
                        .addClass("action-button btn delete-button w-100")
                        .text("Delete Main Thread")
                        .attr("data-game-id", thread.game_id);
                    accordionBody.append(deleteButton);

                    accordionCollapse.append(accordionBody);

                    accordionItem.append(accordionHeader).append(accordionCollapse);
                    searchCreatedMainThreads.append(accordionItem);
                });
            },
        });
    });

    // When a publish button is clicked
    $(document).on("click", ".publish-button", function () {
        var game_id = $(this).data("game-id");  // Get the game id from the button's data

        var visibilityStates = {}; // Initialize an object to store the visibility states
        var checkboxes = $("#thread-" + game_id + " .form-check-input"); // Get all checkboxes for the thread

        checkboxes.each(function () {
            var field = $(this).attr("id").replace("Switch", ""); // Get the field name from the checkbox id
            var is_checked = $(this).is(":checked"); // Check if the checkbox is checked
            visibilityStates[field] = is_checked; // Store the visibility state for the field
        });

        // Send an AJAX request to the server to update and publish the thread
        $.ajax({
            url: "/update_and_publish_thread/",
            method: "POST",
            data: {
                game_id: game_id,
                visibility_states: JSON.stringify(visibilityStates),
                csrfmiddlewaretoken: getCookie("csrftoken"),
            },
            success: function (response) {
                var toastEl = document.getElementById("notificationToast");
                var toast = new bootstrap.Toast(toastEl);
                toastEl.querySelector(".toast-body").textContent = response.status;
                toast.show(); // Show a toast notification with the server's response
            },
            error: function (response) {
                var toastEl = document.getElementById("notificationToast");
                var toast = new bootstrap.Toast(toastEl);
                toastEl.querySelector(".toast-body").textContent =
                    response.responseJSON.error;
                toast.show(); // Show a toast notification with the server's error message
            },
        });
    });

    // When an unpublish button is clicked
    $(document).on("click", ".unpublish-button", function () {
        var game_id = $(this).data("game-id"); // Get the game id from the button's data

        var visibilityStates = {}; // Initialize an object to store the visibility states
        var checkboxes = $("#thread-" + game_id + " .form-check-input"); // Get all checkboxes for the thread

        // For each checkbox
        checkboxes.each(function () {
            var field = $(this).attr("id").replace("Switch", "");
            var is_checked = $(this).is(":checked");
            visibilityStates[field] = is_checked;
        });

        // Send an AJAX request to the server to update and unpublish the thread
        $.ajax({
            url: "/update_and_unpublish_thread/",
            method: "POST",
            data: {
                game_id: game_id,
                visibility_states: JSON.stringify(visibilityStates),
                csrfmiddlewaretoken: getCookie("csrftoken"),
            },
            success: function (response) {
                var toastEl = document.getElementById("notificationToast");
                var toast = new bootstrap.Toast(toastEl);
                toastEl.querySelector(".toast-body").textContent = response.status;
                toast.show();
            },
            error: function (response) {
                var toastEl = document.getElementById("notificationToast");
                var toast = new bootstrap.Toast(toastEl);
                toastEl.querySelector(".toast-body").textContent =
                    response.responseJSON.error;
                toast.show();
            },
        });
    });

    // When a delete button is clicked
    $(document).on("click", ".delete-button", function () {
        var game_id = $(this).data("game-id");
        var button = $(this);

        $("#deleteModal").modal("show"); // Show the delete confirmation modal

        // When the confirm delete button is clicked
        $("#confirmDelete").off("click").on("click", function () {
            // Send an AJAX request to the server to delete the thread
            $.ajax({
                url: "/delete_a_main_thread/",
                method: "POST",
                data: {
                    game_id: game_id,
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                },
                success: function () {
                    button.closest(".accordion-item").remove(); // Remove the thread from the page
                    $("#deleteModal").modal("hide"); // Hide the delete confirmation modal
                },
            });
        });
    });
});

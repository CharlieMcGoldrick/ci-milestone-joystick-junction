$(document).ready(function () {
    $("#searchFormFindGame").on("submit", function (e) {
        e.preventDefault();

        var formData = $(this).serializeArray();

        $.ajax({
            url: $(this).data("url"),
            data: $(this).serialize(),
            success: function (data) {
                var searchGamesForMainThread = $("#searchGamesForMainThread");
                searchGamesForMainThread.empty();

                $.each(data, function (i, game) {
                    var listItem = $("<li>").addClass("result-item");
                    if (i === 0) {
                        listItem.addClass("first-result-item");
                    }

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
                    form.append(
                        $("<button>")
                            .addClass("result-button btn btn-primary w-100")
                            .text("Create Main Thread " + game.name)
                    );

                    listItem.append(form);
                    searchGamesForMainThread.append(listItem);
                });
            },
        });
    });

    $(document).on("submit", ".create-thread-form", function (e) {
        e.preventDefault();

        var formData = $(this).serializeArray();
        var jsonData = {};

        $.each(formData, function (i, field) {
            jsonData[field.name] = field.value;
        });

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

    $("#searchFormMainThread").on("submit", function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).data("url"),
            data: $(this).serialize(),
            success: function (data) {
                var searchCreatedMainThreads = $("#searchCreatedMainThreads");
                searchCreatedMainThreads.empty();

                $.each(data, function (i, thread) {
                    var accordionItem = $("<div>")
                        .addClass("accordion-item mb-3")
                        .attr("id", "thread-" + thread.game_id);

                    var accordionHeader = $("<h2>")
                        .addClass("accordion-header")
                        .attr("id", "heading" + i);
                    var accordionButton = $("<button>")
                        .addClass("accordion-button collapsed")
                        .attr("type", "button")
                        .attr("data-bs-toggle", "collapse")
                        .attr("data-bs-target", "#collapse" + i)
                        .attr("aria-expanded", "false")
                        .attr("aria-controls", "collapse" + i)
                        .text(thread.name);
                    accordionHeader.append(accordionButton);

                    var accordionCollapse = $("<div>")
                        .attr("id", "collapse" + i)
                        .addClass("accordion-collapse collapse")
                        .attr("aria-labelledby", "heading" + i)
                        .attr("data-bs-parent", "#searchCreatedMainThreads");
                    var accordionBody = $("<div>").addClass("accordion-body");

                    var fields = [
                        "name",
                        "summary",
                        "genres",
                        "platforms",
                        "involved_companies",
                        "game_engines",
                        "aggregated_rating",
                    ];
                    $.each(fields, function (j, field) {
                        var infoRow = $("<div>").addClass("info-row row");

                        var formattedField = field
                            .replace(/_/g, " ")
                            .replace(/\b\w/g, function (l) {
                                return l.toUpperCase();
                            });

                        var titleCol = $("<div>")
                            .addClass("info-title col")
                            .text(formattedField);
                        var dataCol = $("<div>").addClass("info-data col");
                        if (
                            [
                                "genres",
                                "platforms",
                                "involved_companies",
                                "game_engines",
                            ].includes(field) &&
                            thread[field]
                        ) {
                            var parsedData = JSON.parse(thread[field]);
                            var names = parsedData
                                .map((item) => item.name || item.company.name)
                                .join(", ");
                            dataCol.text(names);
                        } else if (field === "aggregated_rating" && thread[field]) {
                            dataCol.text(Math.floor(thread[field])); // Round down the rating
                        } else if (thread[field]) {
                            dataCol.text(thread[field]);
                        } else {
                            dataCol.text("N/A");
                        }

                        var switchCol = $("<div>").addClass("info-toggle col form-switch");
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

                        accordionBody.append(infoRow);
                    });

                    var publishButton = $("<button>")
                        .addClass("action-button btn publish-button w-50")
                        .text("Publish Main Thread")
                        .attr("data-game-id", thread.game_id);
                    accordionBody.append(publishButton);

                    var deleteButton = $("<button>")
                        .addClass("action-button btn delete-button w-50")
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

    $(document).on("click", ".publish-button", function () {
        var game_id = $(this).data("game-id");

        var visibilityStates = {};
        var checkboxes = $("#thread-" + game_id + " .form-check-input");

        checkboxes.each(function () {
            var field = $(this).attr("id").replace("Switch", "");
            var is_checked = $(this).is(":checked");
            visibilityStates[field] = is_checked;
        });

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

    $(document).on("click", ".delete-button", function () {
        var game_id = $(this).data("game-id");
        var button = $(this);

        $("#deleteModal").modal("show");

        $("#confirmDelete").off("click").on("click", function () {
            $.ajax({
                url: "/delete_a_main_thread/",
                method: "POST",
                data: {
                    game_id: game_id,
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                },
                success: function () {
                    button.closest(".accordion-item").remove();
                    $("#deleteModal").modal("hide");
                },
            });
        });
    });
});

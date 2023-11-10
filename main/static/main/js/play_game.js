$(document).ready(function() {
    function updateTeamScore(teamId) {
        let totalScore = 0.0;
        $(`.player-score[id^="team${teamId}_points_"]`).each(function() {
            totalScore += parseFloat($(this).text());
        });

        // Update the team's scoreboard
        $(`#team${teamId}_points_total`).text(totalScore.toFixed(1));
    }

    // Initialize Select2 for each player dropdown
    $('[id^="team1_player_"], [id^="team2_player_"]').each(function() {
        var position = $(this).data('pos');

        $(this).select2({
            minimumInputLength: 1,
            language: {
                inputTooShort: function(args) {
                    return "";
                }
            },
            ajax: {
                url: "/api/players/search/" + position + "/",
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        q: params.term,
                    };
                },
                processResults: function(data) {
                    return {
                        results: $.map(data, function(player) {
                            return {
                                id: player.uid,
                                text: player.name + " " + player.pos + " " + player.years_played
                            };
                        })
                    };
                }
            }
        });
    })
    
    
    // On player being selected from dropdown
    $('[id^="team1_player_"], [id^="team2_player_"]').on('select2:select', function (e) {
        var selectedPlayerId = e.params.data.id;
        var correspondingYearDropdown = $(this).closest('.dropdowns').find('select[name$="_year_' + $(this).attr('id').split('_').pop() + '"]');

        // Get the years for the selected player
        $.get("/api/players/" + selectedPlayerId + "/", function(data) {
            var years = [""];

            for (let i = 1970; i <= 2022; i++) {
                var field_name = "fp_" + i.toString();
                if (data[field_name] != null) {
                    years.push(i);
                }
            }

            // Clear existing options and add the new ones
            correspondingYearDropdown.empty();

            $.each(years, function(index, year) {
                correspondingYearDropdown.append(new Option(year, year));
            });
        });
    });


    $(".submit-button").on("click", function() {
        // Get the corresponding dropdown values
        let dataId = $(this).attr("data-id");
        let teamId = $(this).attr("team-id");
        let playerId = $("#team" + teamId + "_player_" + dataId).val();
        let year = $("#team" + teamId + "_year_" + dataId).val();

        // Check if either Player or Year dropdown is not selected
        if(!playerId || !year) {
            return;
        }

        // Construct the API endpoint
        let apiUrl = `/api/players/${playerId}/${year}/`;

        // Make the AJAX request
        $.get(apiUrl, function(data) {
            let points = data.points;

            // Update the corresponding player-score div
            $("#team" + teamId + "_points_" + dataId).text(points);

            // Call the updateTeamScore function
            updateTeamScore(teamId);

        }).fail(function() {
            // Handle any errors, like player not found
            $("#team" + teamId + "_points_" + dataId).text("0.0");
        });

        // Hide the Submit button and show the Remove button
        $(this).hide();
        $(this).siblings(".remove-button").show();
    });

    
    $(".remove-button").on("click", function() {
        let teamId = $(this).attr("team-id");
        let dataId = $(this).attr("data-id")
        let playerId = "team" + teamId + "_player_" + dataId;
        let yearId = "team" + teamId + "_year_" + dataId;
        let pointsId = "team" + teamId + "_points_" + dataId;

        // Reset the dropdowns
        $("#" + playerId).val(null).trigger('change');
        $("#" + yearId).val(null).trigger('change');

        // Reset the player point value
        $("#" + pointsId).text("0.0");

        // Update the team scoreboard
        updateTeamScore(teamId);

        // Hide the Remove button and show the Submit button
        $(this).hide();
        $(this).siblings(".submit-button").show();
    });
});

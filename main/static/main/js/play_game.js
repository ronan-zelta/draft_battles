$(document).ready(function() {
    // Initialize Select2 for each player dropdown
    $('[id^="team1_player_"], [id^="team2_player_"]').select2({
        minimumInputLength: 1,
        language: {
            inputTooShort: function(args) {
                return "";
            }
        },
        ajax: {
            url: "/api/players/search/",
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

    $(".submit-button").on("click", function() {
        // Get the corresponding dropdown values
        let dataId = $(this).attr("data-id");
        let teamId = $(this).attr("team-id");
        let playerId = $("#team" + teamId + "_player_" + dataId).val();
        let year = $("#team" + teamId + "_year_" + dataId).val();

        // Construct the API endpoint
        let apiUrl = `/api/players/${playerId}/${year}/`;

        // Make the AJAX request
        $.get(apiUrl, function(data) {
            // Assuming the response has a field named "points"
            let points = data.points;

            // Update the corresponding player-score div
            $("#team" + teamId + "_points_" + dataId).text(points);
        }).fail(function() {
            // Handle any errors, like player not found
            $("#team" + teamId + "_points_" + dataId).text("0.0");
        });
    });

    
    // Event listener when a player is selected
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
});

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
    $('.player-dropdown').each(function() {
        var position = $(this).data('pos');
		var fontSize = $(window).width() <= 768 ? '1.3vh' : '2.5vh';

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
            },
			templateResult: function(state) {
                if (!state.id) {
                    return state.text;
                }
                // Split the text into parts (assuming the format is 'name pos years_played')
                var parts = state.text.split(" ");
                var name = parts.slice(0, -2).join(" "); // Player's name
                var posYears = parts.slice(-2).join("  "); // Player's position and years played

                // Create a flex container for the text
                var $state = $(`
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: ${fontSize}; text-align: left;">${name}</span>
                        <span style="font-size: ${fontSize}; text-align: right;">${posYears}</span>
                    </div>
                `);
                return $state;
            },
            templateSelection: function(state) {
                // Similar approach for the selected item
                if (!state.id) {
                    return state.text;
                }
                var parts = state.text.split(" ");
                var name = parts.slice(0, -2).join(" ");
                var posYears = parts.slice(-2).join("  ");

                return $(`
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: ${fontSize}; text-align: left;">${name}</span>
                        <span style="font-size: ${fontSize}; text-align: right;">${posYears}</span>
                    </div>
                `);
            }
        }).on('select2:open', function (e) {
			const selectId = e.target.id

			$(".select2-search__field[aria-controls='select2-" + selectId + "-results']").each(function (
				key,
				value,
			){
				value.focus();
			})
		});

		// Initialize Select2 for each season dropdown
		$('.season-dropdown').each(function() {
			// Determine font size based on screen width
			var fontSize = $(window).width() <= 768 ? '1.3vh' : '2.5vh';
	
			$(this).select2({
				minimumResultsForSearch: Infinity, // Disable the search box
				templateResult: function(state) {
					if (!state.id) {
						return state.text;
					}
					var $state = $('<span style="font-size: ' + fontSize + ';">' + state.text + '</span>');
					return $state;
				},
				templateSelection: function(state) {
					return $('<span style="font-size: ' + fontSize + ';">' + state.text + '</span>');
				}
			});
		}).prop("disabled", true).next('.select2-container').find('.select2-selection').css('background-color', '#fff');
    })

    // On player being selected from dropdown
    $('.player-dropdown').on('select2:select', function (e) {
        var selectedPlayerId = e.params.data.id;
        var correspondingYearDropdown = $(this).closest('.player-row').find('.season-dropdown');

        // Get the years for the selected player
        $.get("/api/players/" + selectedPlayerId + "/", function(data) {
            var years = [""];

            for (let i = 1970; i <= 2023; i++) {
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

		$(this).closest('.player-row').find('.season-dropdown').prop("disabled", false);
    });


    $(".submit-button").on("click", function() {
        // Get the corresponding dropdown values
        let dataId = $(this).attr("data-id");
        let teamId = $(this).attr("team-id");
        let playerId = $(this).closest('.player-row').find('.player-dropdown').val();
        let year = $(this).closest('.player-row').find('.season-dropdown').val();

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
        let playerRow = $(this).closest('.player-row');
        let playerId = playerRow.find('.player-dropdown').attr('id');
        let yearId = playerRow.find('.season-dropdown').attr('id');
        let pointsId = "team" + teamId + "_points_" + playerRow.find('.player-dropdown').attr('id').split('_').pop();

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

    $("#edit-score-btn").on("click", function() {
        $("#edit-score-popup").show();
    });

    $(".close-edit-score-button").on("click", function() {
        $("#edit-score-popup").hide();
    });
});

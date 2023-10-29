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

});

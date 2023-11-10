$(document).ready(function() {
    // On 'How to Play' button click, show popup
    $(".how-to-btn").on("click", function() {
        $("#how-to-popup").show();
    });
    // On close button click, hide popup
    $(".close-how-to-button").on("click", function() {
        $("#how-to-popup").hide();
    });

    // On 'Buy Me a Beer' button click, show popup
    $(".beer-btn").on("click", function() {
        $("#beer-popup").show();
    });
    // On close button click, hide popup
    $(".close-beer-button").on("click", function() {
        $("#beer-popup").hide();
    });
});
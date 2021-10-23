var select = document.querySelector("select");
var button = document.querySelector(".filter-button input[type=submit]")
function show_options() {
    var options = document.querySelectorAll(".options");
    for (var i = 0; i < options.length; i++) {
        options[i].style.display = "block";
    }
}
select.addEventListener("change", function(e) {
    button.click();
});
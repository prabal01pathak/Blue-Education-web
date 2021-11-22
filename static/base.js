var navLogo = document.querySelector('.nav-bar');
var navLinks = document.querySelector(".nav-links");
var nav1st = document.querySelector(".nav-1st");
var nav2nd = document.querySelector(".nav-2nd");
var nav3rd = document.querySelector(".nav-3rd");
var navButton = document.querySelectorAll(".extra-links-button");
var embedLinks = document.querySelectorAll(".extra-links");

navLogo.addEventListener("click", () => {
    navLogo.classList.toggle("nav-bar-active");
    navLinks.classList.toggle("translate-navbar");

});



navButton.forEach((button,index) => {
    button.addEventListener("click", () => {
        embedLinks[index].classList.toggle("extra-links-show");
        button.classList.toggle("extra-links-button-rotate");
    });
});
    

var selectAll = document.querySelector(".select-all input[type=checkbox]");
var selectAllCheckbox = document.querySelectorAll("form .questions input[type=checkbox]");
var assignSelect = document.querySelector("#do-action"); 
var assignThings = document.querySelector("form .assign-things"); 
var assignThingsHide = document.querySelector(".assign_title_button");


selectAll.addEventListener("click", function() {
    for (var i = 0; i < selectAllCheckbox.length; i++) {
        if (selectAllCheckbox[i].checked) {
            selectAllCheckbox[i].checked = false;
        }else{
        selectAllCheckbox[i].checked = true;
        };
    }
});

//Assign items to other papers
assignSelect.addEventListener("click", function() {
    var assign = assignSelect.value;
    if (assign == "assign_to_other") {
        assignThings.style.transform = "translateX(0%)"; 
    }else {
        assignThings.style.transform = "translateX(100%)";
    };
});

assignThingsHide.addEventListener("click",() => {
	assignThings.style.transform="translateX(100%)";
});

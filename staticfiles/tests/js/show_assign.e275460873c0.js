var selectAll = document.querySelector(".select-all input[type=checkbox]");
var selectAllCheckbox = document.querySelectorAll("form .questions input[type=checkbox]");
var assignSelect = document.querySelector("#do-action"); 
var assignThings = document.querySelector("form .assign-things"); 

selectAll.addEventListener("click", function() {
    for (var i = 0; i < selectAllCheckbox.length; i++) {
        if (selectAllCheckbox[i].checked) {
            selectAllCheckbox[i].checked = false;
        }else{
        selectAllCheckbox[i].checked = true;
        };
    }
});

assignSelect.addEventListener("change", function() {
    var assign = assignSelect.value;
    console.log(assign);
    if (assign == "assign_to_other") {
        console.log("assign to other");
        assignThings.style.transform = "translateX(0%)"; 
    }else {
        console.log("assign to self");
        assignThings.style.transform = "translateX(100%)";
    };
});


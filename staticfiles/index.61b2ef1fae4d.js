/*
    * global variables
*/

var questionsLinks = document.querySelector('.questions-links'); 
var upArrow = document.querySelector('.up-arrow');
var questions = document.querySelectorAll('.question');
var radioCheck = document.querySelectorAll('.radio-check');
var upArrow = document.querySelector('.up-arrow');
var instruction = document.querySelector('.instructions'); 
var main =  document.querySelector('.main');
var questionForm = document.querySelector('#form'); 



/* bring question updated list on click uparrow */

radioCheck.forEach((item) => {
    upArrow.addEventListener('click', (e) => {
        elementN = item.getAttribute('name');
        try {
            elements = document.getElementsByName(elementN);
            if (elements[1].getAttribute('type') == 'radio') {
                var check = document.querySelectorAll(`input[name=${elementN}]:checked`);
                if (check.length ==0) {
                    item.style.backgroundColor  = 'rgb(55,55,233)'; 
                };
            }else {
                if (elements[1].getAttribute('type') == "text") {
                    if (elements[1].value == "") {
                        item.style.backgroundColor  = 'rgb(55,55,233)'; 
                    }else {
                        item.style.backgroundColor  = 'green';
                    };
                }
            };
        }catch(e) {
            var write = document.querySelector(`input[name=${elementN}]`);
            if (write.value == "") {
                write.style.backgroundColor = 'rgb(55,55,233)';
            };
        };
    });
});

/* ========================== */

questions.forEach((item,index) => { 
    item.addEventListener('click', () => {
        element = radioCheck[index];
        elementName = element.getAttribute('name');
        try{
            var written = document.querySelector(`input[name=${elementName}]`);
            if ( written.type == "radio") {
                var checked = document.querySelector(`input[name=${elementName}]:checked`);
                if (checked != null) {
                radioCheck[index].style.backgroundColor = 'green';
                }else {
                    radioCheck[index].style.backgroundColor = 'rgb(55,55,233)';
                };
            }else if (written.type == "text") {
                if (written.value != "") {
                    radioCheck[index].style.backgroundColor = 'blue';
                }else {
                    radioCheck[index].style.backgroundColor = 'rgb(55,55,233)';
                };
            };
        } catch(err) {
            console.log(err);
        };
    });
   
});
function timer(time) {
    var timer = document.querySelector('.clock');
    var minute = time-1;
    var second = 60;
    var interval = setInterval(function() {
        if (minute < 1 && second < 1) {
            clearInterval(interval);
            timer.innerHTML = "Time's up!";
            var submitButton = document.querySelector('input[type=submit]'); 
            submitButton.click();
        };
        second--;
        if (second<10) {
            var show_second = `0${second}`;
            timer.innerHTML = `${minute}:${show_second}`;
        }else {
            timer.innerHTML = `${minute}:${second}`;
        };
        if (minute<10){
            var show_minute = `0${minute}`
            timer.innerHTML = `${show_minute}:${second}`;
        }else{
            timer.innerHTML = `${minute}:${second}`;
        };
        if (second == 0 && minute != 0) {
            minute--;
            second = 60;
        };
    }, 1000);
}

/* Accept instructions and show question if it is valid selection */

function accept_instructions() {
    var checkBox = document.querySelector("input[type=checkbox]");
    var instructionsWindow = document.querySelector(".instructions")
    if (checkBox.checked) {
        instructionsWindow.style.display = "none";
        questionForm.style.display = "block";
        var studentHours = document.querySelector('.student-hours'); 
        var value = studentHours.innerText;
        timer(parseInt(value));
    }
};

/* =============== */
    


upArrow.addEventListener("click",() => {
    questionsLinks.classList.toggle('show-links');
    upArrow.classList.toggle('rotate-arrow');
});

questionsLinks.addEventListener("click",() => {
    questionsLinks.classList.toggle('show-links');
    upArrow.classList.toggle('rotate-arrow');
});


function checkedRadio() {
    var radioCheckedName = document.querySelectorAll('input[type="radio"]:checked');
    var radio = document.querySelectorAll('input[type="radio"]');
    radio.forEach((item) => {
        item.addEventListener("click",() => {
            radioButton = item.name
            var question = document.getElementsByName(radioButton);
            console.log(item.checked);
            if (item.checked) {
                question[0].style.backgroundColor = 'green';
            }else {
                question[0].style.backgroundColor = "blue";
            };
        });

    });
};


try {
    var button = document.querySelector("#startButton");
    button.addEventListener("click", accept_instructions);
} catch (error) {
    console.log(error);
};
var instructions = document.querySelectorAll('.instructions');
console.log(instructions.length);
if (instructions.length == 1) {
    questionForm.style.display = "none";
    console.log(questionForm)
}

$("navbar-toggler").blur( () => {
   $("collapse").collapse('hide'); 
    console.log("collapse");
})

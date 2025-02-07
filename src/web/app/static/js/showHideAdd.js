document.addEventListener("DOMContentLoaded", function () {
    showHideAdd();
});

function showHideAdd(){
    var addToggle = document.getElementById("showAdd");
    var addText = document.getElementById("addText"); 
    var addList = document.getElementById("addskillList");

    addToggle.addEventListener('click', function(e){
        if (addToggle.checked){
            addList.style.display = "flex";
            addText.innerHTML = "Hide Additional Skills"
        } else{
            addList.style.display = "none";
            addText.innerHTML = "Show Additional Skills"
        }
    });
}

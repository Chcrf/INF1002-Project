document.addEventListener("DOMContentLoaded", function () {
    showHideCore();
    showHideAdd();
});

function showHideCore(){
    var coreToggle = document.getElementById("showCore");
    var coreText = document.getElementById("coreText");
    var coreList = document.getElementById("coreskillList");

    coreToggle.addEventListener('click', function(e){
        if (coreToggle.checked){
            coreList.style.display = "flex";
            coreText.innerHTML = "Hide Core Skills"
        } else{
            coreList.style.display = "none";
            coreText.innerHTML = "Show Core Skills"
        }
    });
}

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

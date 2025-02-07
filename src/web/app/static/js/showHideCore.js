document.addEventListener("DOMContentLoaded", function () {
    showHideCore();
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

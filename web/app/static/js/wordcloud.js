document.addEventListener("DOMContentLoaded", function () {
    displayWordcloud();
    
});

function displayWordcloud(){
    fetch('json/top10skills.json')
    .then(response => response.json())
    .then(data => {
        jdata = data
        const scaleFactor = 60;
        const scaledData = jdata.map(item => [item[0], Math.round(item[1] / scaleFactor)]);
        getcloud(scaledData)
        })
    .catch(error => console.error("Error loading JSON:", error));

    function getcloud(word){
        var parentDiv = document.querySelector(".carousel-item.active .carousel-graph");
        var canvas = document.getElementById("wordcloud");
    
        canvas.height = parentDiv.offsetHeight;
        canvas.width = parentDiv.offsetWidth;
    
        if (canvas) {
            WordCloud(canvas, {
                list: word,
                gridSize: 10,
                weightFactor: 1,
                fontFamily: "Arial",
                color: "random-dark",
                backgroundColor: "#F3D250"
            });
        }
    }
}
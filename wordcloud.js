
document.addEventListener("DOMContentLoaded", function () {
    fetch('top10skills.json')
    .then(response => response.json())
    .then(data => {
        jdata = data
        const scaleFactor = 60;
        const scaledData = jdata.map(item => [item[0], Math.round(item[1] / scaleFactor)]);
        getcloud(scaledData)
        })
    .catch(error => console.error("Error loading JSON:", error));
    
    function getcloud(word){
        var canvas = document.getElementById("wordcloud");

        if (canvas) {
            WordCloud(canvas, {
                list: word,
                gridSize: 10,
                weightFactor: 1,
                fontFamily: "Arial",
                color: "random-dark",
                backgroundColor: "#ffffff"
            });
        }
    }
});

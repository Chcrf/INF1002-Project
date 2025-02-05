document.addEventListener("DOMContentLoaded", function () {
    var words = [
        ["Python", 12],
        ["HTML", 10],
        ["CSS", 8],
        ["JavaScript", 15],
        ["WordCloud", 20],
        ["Django", 7],
        ["Flask", 5],
        ["React", 10],
        ["Node.js", 8],
        ["AI", 12]
    ];

    var parentDiv = document.getElementById("graph1");
    var canvas = document.getElementById("wordcloud");

    canvas.height = parentDiv.offsetHeight;
    canvas.width = parentDiv.offsetWidth;

    if (canvas) {
        WordCloud(canvas, {
            list: words,
            gridSize: 10,
            weightFactor: 5,
            fontFamily: "Arial",
            color: "random-dark",
            backgroundColor: "#90ccf4"
        });
    }
});

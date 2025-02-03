carouselColor = {
    "carousel1": "#F3D250",
    "carousel2": "#90CCF4",
    "carousel3": "#F78888",
}

document.addEventListener("DOMContentLoaded", function () {
    carouselEdit();
    carouselBgColorChange();

});

function carouselEdit() {
    let carouselMain = document.querySelector("#main"); // Select carousel

    function UpdateLeftandRightHTML() {
        let activeItem = document.querySelector('.carousel-item.active');
        let activeID = activeItem.id

        if (activeID == 'carousel1') {
            prevID = 'carousel3'
            nextID = 'carousel2'
        } else if (activeID == 'carousel2') {
            prevID = 'carousel1'
            nextID = 'carousel3'
        } else if (activeID == 'carousel3') {
            prevID = 'carousel2'
            nextID = 'carousel1'
        }

        var leftSide = document.querySelector("#leftCarousel");
        var rightSide = document.querySelector("#rightCarousel");

        // Add background colors to side carousels
        leftSide.style.backgroundColor = carouselColor[prevID]
        rightSide.style.backgroundColor = carouselColor[nextID]

        // leftSide.innerHTML = document.getElementById(prevID).innerHTML;
        // rightSide.innerHTML = document.getElementById(nextID).innerHTML;

    }

    function transformDirection(e) {
        let direction = e.direction;
        let leftSide = document.querySelector("#leftCarousel");
        let rightSide = document.querySelector("#rightCarousel");

        // Remove first load CSS
        leftSide.classList.remove('translateLeft');
        rightSide.classList.remove('translateRight');

        // Remove for transition to work
        leftSide.classList.remove('leftTransformLeft');
        rightSide.classList.remove('leftTransformRight');
        rightSide.classList.remove('rightTransformRight');
        leftSide.classList.remove('rightTransformLeft');

        if (direction == "left") {
            leftSide.classList.remove('left');
            // Set left transform from middle to left
            // Delay to set transition
            setTimeout(() => {
                leftSide.classList.add('leftTransformLeft');
                // Add blur?
                //leftSide.style.filter = 'blur(2px)';
            }, 10);

            // Set right beginning position (right outside screen)
            rightSide.classList.add('right');
            // Set right transform from right to right with a bit of space
            setTimeout(() => {
                rightSide.classList.add('leftTransformRight');
                // Add blur?
                //rightSide.style.filter = 'blur(2px)';
            }, 10);

        } else if (direction == "right") {
            rightSide.classList.remove('right');

            // Set right transform from middle to right
            setTimeout(() => {
                rightSide.classList.add('rightTransformRight');
                // Add blur?
                //rightSide.style.filter = 'blur(2px)';
            }, 10);

            // Set left beginning position (left outside screen)
            leftSide.classList.add('left');
            // Set left transform from left to left with a bit of space
            setTimeout(() => {
                leftSide.classList.add('rightTransformLeft');
                // Add blur?
                //leftSide.style.filter = 'blur(2px)';
            }, 10);
        }

    }

    UpdateLeftandRightHTML();

    carouselMain.addEventListener('slid.bs.carousel', function (event) {
        UpdateLeftandRightHTML();
        transformDirection(event);
    })
}

function carouselBgColorChange() {
    let carousel = document.querySelector("#main");

    let carouselItems = carousel.querySelectorAll(".carousel-item");
    for (let item of carouselItems) {
        let id = item.id;
        item.style.backgroundColor = carouselColor[id];
    }
}
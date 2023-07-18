var imageWidthHalf, imageHeightHalf;

var canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
canvas.style.display = 'block';
document.body.appendChild(canvas);

var context = canvas.getContext('2d');

var image = document.createElement('img');

image.addEventListener(
    'load',
    function () {
        imageWidthHalf = Math.floor(this.width / 2);
        imageHeightHalf = Math.floor(this.height / 2);

        document.addEventListener('mousemove', onMouseEvent, false);
        document.addEventListener('touchstart', onTouchEvent, false);
        document.addEventListener('touchmove', onTouchEvent, false);
    },
    false
);

// Or any other image URI
image.src = 'data:image/png;base64,...';

function onMouseEvent(event) {
    context.drawImage(image, event.clientX - imageWidthHalf, event.clientY - imageHeightHalf);
}

function onTouchEvent(event) {
    event.preventDefault();

    for (var i = 0; i < event.touches.length; i++) {
        context.drawImage(
            image,
            event.touches[i].pageX - imageWidthHalf,
            event.touches[i].pageY - imageHeightHalf
        );
    }
}
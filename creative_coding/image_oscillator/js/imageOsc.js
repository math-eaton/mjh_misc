let context;
let oscillator;
let minBrightness;
let maxBrightness;

function calculateBrightnessRange(img) {
  minBrightness = 255;
  maxBrightness = 0;

  img.loadPixels();
  for (let i = 0; i < img.pixels.length; i += 4) {
    let r = img.pixels[i];
    let g = img.pixels[i + 1];
    let b = img.pixels[i + 2];
    let brightnessValue = (r + g + b) / 3; // Simple average for brightness

    if (brightnessValue < minBrightness) {
      minBrightness = brightnessValue;
    }
    if (brightnessValue > maxBrightness) {
      maxBrightness = brightnessValue;
    }
  }

  console.log("Min Brightness:", minBrightness);
  console.log("Max Brightness:", maxBrightness);
}

function updateFrequencyDisplay(freq) {
  let freqDisplay = document.getElementById('frequencyDisplay');
  freqDisplay.textContent = `${freq.toFixed(1)} Hz`;
}


function setup() {
  let cnv = select('#map');
  resizeCanvas(1500, 1100);
  cnv.elt.willReadFrequently = true;
  
  loadImage('assets/propagation_Raster.png', img => {
    image(img, 0, 0, width, height);
    calculateBrightnessRange(img); // Calculate the brightness range after loading the image
  });
  
  noLoop();
}

let gainNode;

function startAudio() {
  context = new AudioContext();
  oscillator = context.createOscillator();
  gainNode = context.createGain(); // Create the gain node

  oscillator.type = 'sine';
  oscillator.connect(gainNode); // Connect the oscillator to the gain node
  gainNode.connect(context.destination); // Connect the gain node to the speakers

  oscillator.start();
  loop(); // Starts the draw loop
}

const WHOLE_TONE_SCALE = [
  130.81, // C3
  146.83, // D3
  164.81, // E3
  185.00, // F#3
  207.65, // G#3
  233.08, // A#3
];

let prevColor = null;
const COLOR_CHANGE_THRESHOLD = 100; // Adjust this value as needed

function setColorBasedFrequency(col) {
  let brightnessValue = brightness(col);
  
  // Map the brightness to a frequency range, for example, 100Hz to 1000Hz
  let freq = map(brightnessValue, 0, 255, 100, 1000);
  
  oscillator.frequency.setValueAtTime(freq, context.currentTime);
  updateFrequencyDisplay(freq); // Update the frequency display below the image


  // Check for significant color change
  if (!prevColor || dist(red(prevColor), green(prevColor), blue(prevColor), red(col), green(col), blue(col)) > COLOR_CHANGE_THRESHOLD) {
    // Apply the 2ms attack envelope only if there's a significant color change
    gainNode.gain.cancelScheduledValues(context.currentTime);
    gainNode.gain.setValueAtTime(gainNode.gain.value, context.currentTime); // Start from the current gain value
    gainNode.gain.linearRampToValueAtTime(0, context.currentTime + 0.01); // Quickly fade out
    gainNode.gain.linearRampToValueAtTime(1, context.currentTime + 0.03); // Then fade in over 2ms
    prevColor = col; // Update the previous color only when a significant change is detected
  }
}

function draw() {
  if (oscillator) { // Check if oscillator is defined
    let col = get(mouseX, mouseY);
    setColorBasedFrequency(col);
    console.log(col)
  }
}


document.getElementById('startButton').addEventListener('click', function() {
  startAudio();
  document.getElementById('map').style.display = 'block'; // Display the canvas
  this.style.display = 'none'; // hides the button after it's clicked
});
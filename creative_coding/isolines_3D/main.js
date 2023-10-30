// Import modules
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import proj4 from 'proj4';

// Define the custom projection with its PROJ string
const statePlaneProjString = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";
proj4.defs("EPSG:32118", statePlaneProjString);

// Use this function to convert lon/lat to State Plane coordinates
function toStatePlane(lon, lat) {
  if (!Number.isFinite(lon) || !Number.isFinite(lat)) {
    throw new Error(`Invalid coordinates: longitude (${lon}), latitude (${lat})`);
  }
  return proj4("EPSG:32118").forward([lon, lat]);
}

// Three.js - Initialize the Scene
let scene, camera, renderer, controls;

function initThreeJS() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 50; // Adjust as necessary
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('three-container').appendChild(renderer.domElement);
    controls = new OrbitControls(camera, renderer.domElement);
    let ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    let directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(0, 1, 0);
    scene.add(directionalLight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
    console.log("animating")
}

initThreeJS();
animate();

// Define a scaling factor for the Z values (elevation)
const zScale = 0.0005; // Change this value to scale the elevation up or down

// Function to get color based on elevation
function getColorForElevation(elevation, minElevation, maxElevation) {
  const gradient = [
    { stop: 0, color: new THREE.Color(0x0000ff) }, // blue at the lowest
    { stop: 0.5, color: new THREE.Color(0x00ff00) }, // green at the middle
    { stop: 1, color: new THREE.Color(0xff0000) }  // red at the highest
  ];

  const t = (elevation - minElevation) / (maxElevation - minElevation);

  let lowerStop = gradient[0], upperStop = gradient[gradient.length - 1];
  for (let i = 0; i < gradient.length - 1; i++) {
    if (t >= gradient[i].stop && t <= gradient[i + 1].stop) {
      lowerStop = gradient[i];
      upperStop = gradient[i + 1];
      break;
    }
  }

  const color = lowerStop.color.clone().lerp(upperStop.color, (t - lowerStop.stop) / (upperStop.stop - lowerStop.stop));
  return color;
}

// Updated function to add contour lines with gradient colors
function addContourLines(geojson) {
  // Determine min and max elevation from the geojson
  const elevations = geojson.features.map(f => f.properties.Contour);
  const minElevation = Math.min(...elevations);
  const maxElevation = Math.max(...elevations);

  geojson.features.forEach((feature, index) => {
    const contour = feature.properties.Contour; // Elevation value
    const coordinates = feature.geometry.coordinates; // Array of [lon, lat] pairs

    const color = getColorForElevation(contour, minElevation, maxElevation);
    let material = new THREE.LineBasicMaterial({ color: color });

    // Function to process a single line
    const processLine = (lineCoords, contourValue) => {
      let vertices = [];
      lineCoords.forEach((pair) => {
        if (!Array.isArray(pair) || pair.length !== 2 || pair.some(c => isNaN(c))) {
          console.error(`Feature ${index} has invalid coordinates`, pair);
          return;
        }
        const [lon, lat] = pair;
        try {
          const [x, y] = toStatePlane(lon, lat);
          const z = contourValue * zScale; // Scale the elevation for visibility
          vertices.push(x, y, z);
        } catch (error) {
          console.error(`Feature ${index} error in toStatePlane:`, error.message);
        }
      });

      if (vertices.length > 0) {
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        const line = new THREE.Line(geometry, material);
        scene.add(line);
      }
    };

    // Check geometry type and process accordingly
    if (feature.geometry.type === 'LineString') {
      processLine(coordinates, contour);
    } else if (feature.geometry.type === 'MultiLineString') {
      coordinates.forEach(lineCoords => {
        processLine(lineCoords, contour);
      });
    } else {
      console.error(`Unsupported geometry type: ${feature.geometry.type}`);
    }
  });
}




function getBoundingBoxOfGeoJSON(geojson) {
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;

  // Function to process each coordinate pair
  const processCoordinates = (coords) => {
    coords.forEach(coord => {
      // If it's a MultiLineString, coord will be an array of coordinate pairs
      if (Array.isArray(coord[0])) {
        processCoordinates(coord); // Recursive call for arrays of coordinates
      } else {
        // Assuming coord is [longitude, latitude]
        const [lon, lat] = coord;

        // Transform the coordinates
        const [x, y] = toStatePlane(lon, lat);

        // Update the min and max values
        minX = Math.min(minX, x);
        maxX = Math.max(maxX, x);
        minY = Math.min(minY, y);
        maxY = Math.max(maxY, y);
      }
    });
  };

  // Iterate over each feature
  geojson.features.forEach(feature => {
    processCoordinates(feature.geometry.coordinates);
  });

  // Return bounding box with min and max as THREE.Vector3 objects
  return {
    min: new THREE.Vector3(minX, minY, -Infinity),
    max: new THREE.Vector3(maxX, maxY, Infinity)
  };
}


function constrainCamera(controls, boundingBox) {
  controls.addEventListener('change', () => {
    // Clamp the camera position within the bounding box
    camera.position.x = Math.max(boundingBox.min.x, Math.min(boundingBox.max.x, camera.position.x));
    camera.position.y = Math.max(boundingBox.min.y, Math.min(boundingBox.max.y, camera.position.y));
    camera.position.z = Math.max(boundingBox.min.z, Math.min(boundingBox.max.z, camera.position.z));
    
    // Clamp the controls target within the bounding box
    controls.target.x = Math.max(boundingBox.min.x, Math.min(boundingBox.max.x, controls.target.x));
    controls.target.y = Math.max(boundingBox.min.y, Math.min(boundingBox.max.y, controls.target.y));
    controls.target.z = Math.max(boundingBox.min.z, Math.min(boundingBox.max.z, controls.target.z));

    // Do NOT call controls.update() here, as it would trigger the 'change' event again
  });
}


// Function to get the center of the bounding box
// This function is correct but make sure it's called after the lines are added to the scene
function getCenterOfBoundingBox(boundingBox) {
  return new THREE.Vector3(
    (boundingBox.min.x + boundingBox.max.x) / 2,
    (boundingBox.min.y + boundingBox.max.y) / 2,
    0 // Assuming Z is not important for centering in this case
  );
}

// Ensure that you get the size correctly
function getSizeOfBoundingBox(boundingBox) {
  return new THREE.Vector3(
    boundingBox.max.x - boundingBox.min.x,
    boundingBox.max.y - boundingBox.min.y,
    boundingBox.max.z - boundingBox.min.z
  );
}

// Adjust the camera to view the entire extent of the GeoJSON features
function adjustCameraToBoundingBox(camera, controls, boundingBox) {
  const center = getCenterOfBoundingBox(boundingBox);
  const size = getSizeOfBoundingBox(boundingBox);
  const maxDim = Math.max(size.x, size.y);
  const fov = camera.fov * (Math.PI / 180);
  let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)); // Adjust the 2 to frame the scene

  cameraZ *= 1.1; // Slight adjustment to ensure the features are fully visible
  camera.position.set(center.x, center.y, cameraZ);
  controls.target.set(center.x, center.y, 0);
  controls.update();
}


// Set material for the contour lines
const lineMaterial = new THREE.LineBasicMaterial({
  color: 0xff0000, // Bright red
  linewidth: 4 // Make sure the lines are thick enough to be visible
});

// After loading the GeoJSON and creating the bounding box
fetch('data/cont49l010a_Clip_SimplifyLin.geojson')
  .then(response => response.json())
  .then(geojson => {
    addContourLines(geojson);
    const boundingBox = getBoundingBoxOfGeoJSON(geojson);
    
    // Move the camera and set controls target
    const center = getCenterOfBoundingBox(boundingBox);
    const size = getSizeOfBoundingBox(boundingBox);
    const maxDim = Math.max(size.x, size.y);
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
    cameraZ *= 1.1; // Slight adjustment
    camera.position.set(center.x, center.y, cameraZ);
    controls.target.set(center.x, center.y, 0);

    // Now, add the constraints to the camera and controls
    constrainCamera(controls, boundingBox);

    // Call this after setting the position and target
    controls.update();
  })
  .catch(error => {
    console.error('Error loading GeoJSON:', error);
  });


// Uncomment these lines to add helpers to the scene
// const axesHelper = new THREE.AxesHelper(5);
// scene.add(axesHelper);

// Call this after you have created the bounding box
// const boxHelper = new THREE.BoxHelper(new THREE.Line(geometry, material));
// scene.add(boxHelper);

// Set the background color after initializing the renderer
renderer.setClearColor(0xaaaaaa); // A neutral gray background



// const axesHelper = new THREE.AxesHelper(5);
// scene.add(axesHelper);

// const boxHelper = new THREE.BoxHelper(new THREE.Mesh(geometry));
// scene.add(boxHelper);

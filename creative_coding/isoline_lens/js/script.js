import MAPBOX_ACCESS_TOKEN from '/js/secret.js';

mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [-74.4641, 44.2239],
    zoom: 11,
    minZoom: 8 
});

let geojsonData = null;

// Load the original GeoJSON data
fetch('data/cont49l010a_Clip_SimplifyLin.geojson')
    .then(response => response.json())
    .then(data => {
        geojsonData = data;

        map.addSource('isoline-data', {
            'type': 'geojson',
            'data': data,
            'maxzoom': 22  // increase the maxzoom level
        });
        
        map.addLayer({
            'id': 'isolines',
            'type': 'line',
            'source': 'isoline-data',
            'paint': {
                'line-color': '#FF0000',
                'line-width': 2
            }
        });
    });

function getLensBounds() {
    const center = map.getCenter();
    const lensSize = 0.01;
    return {
        type: 'Polygon',
        coordinates: [[
            [center.lng - lensSize, center.lat - lensSize],
            [center.lng - lensSize, center.lat + lensSize],
            [center.lng + lensSize, center.lat + lensSize],
            [center.lng + lensSize, center.lat - lensSize],
            [center.lng - lensSize, center.lat - lensSize]
        ]]
    };
}

function flattenMultiLineStrings(feature) {
    if (feature.geometry.type !== 'MultiLineString') {
        return [feature];
    }

    return feature.geometry.coordinates.map(line => {
        return {
            type: "Feature",
            properties: feature.properties,
            geometry: {
                type: "LineString",
                coordinates: line
            }
        };
    });
}

function updateLensData() {
    const lensBounds = getLensBounds();
    const uniqueIntersectingIsolines = new Set();

    geojsonData.features.forEach(feature => {
        const flattenedFeatures = flattenMultiLineStrings(feature);
        
        flattenedFeatures.forEach(flattenedFeature => {
            if (turf.booleanCrosses(flattenedFeature, lensBounds)) {
                uniqueIntersectingIsolines.add(flattenedFeature.id || JSON.stringify(flattenedFeature.geometry));
            }
        });
    });

    // Update the count in the UI
    document.getElementById('count-display').innerText = `Isoline count: ${uniqueIntersectingIsolines.size}`;
}

map.on('moveend', updateLensData);

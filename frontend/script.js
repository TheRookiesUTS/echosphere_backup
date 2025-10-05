// Backend API Configuration
const BACKEND_URL = 'http://localhost:8000';  // FastAPI backend

// City coordinates for the demo
const CITIES = {
    kualalumpur: { lat: 3.1390, lng: 101.6869, name: 'Kuala Lumpur' },
    jakarta: { lat: -6.2088, lng: 106.8456, name: 'Jakarta' },
    manila: { lat: 14.5995, lng: 120.9842, name: 'Manila' },
    bangkok: { lat: 13.7563, lng: 100.5018, name: 'Bangkok' },
    singapore: { lat: 1.3521, lng: 103.8198, name: 'Singapore' },
    hochiminh: { lat: 10.8231, lng: 106.6297, name: 'Ho Chi Minh City' },
    mumbai: { lat: 19.0760, lng: 72.8777, name: 'Mumbai' },
    tokyo: { lat: 35.6762, lng: 139.6503, name: 'Tokyo' }
};

// Global variables
let map;
let currentCity = 'kualalumpur';
let dataLayers = {
    heat: null,
    airQuality: null,
    flood: null,
    green: null,
    growth: null
};
let baseLayers = {
    satellite: null,
    topographic: null,
    terrain: null,
    streets: null
};
let contourLayer = null;
let elevationProfile = null;

// Area selection variables
let selectedArea = null;
let selectionMode = false;
let selectionRectangle = null;
let selectedAreaData = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupEventListeners();
    loadInitialData();
});

// Initialize Leaflet map
function initializeMap() {
    const city = CITIES[currentCity];
    
    map = L.map('map', {
        center: [city.lat, city.lng],
        zoom: 12,
        zoomControl: true,
        attributionControl: true
    });

    // Initialize base layers
    initializeBaseLayers();
    
    // Add default satellite layer
    if (baseLayers.satellite) {
        baseLayers.satellite.addTo(map);
    }
    
    // Add custom controls
    addMapControls();
}

// Add NASA satellite imagery layer
function addNASASatelliteLayer() {
    const city = CITIES[currentCity];
    
    // Fetch NASA Earth imagery
    fetchNASAEarthImagery(city.lat, city.lng)
        .then(data => {
            if (data && data.url) {
                const imageBounds = [
                    [city.lat - 0.1, city.lng - 0.1],
                    [city.lat + 0.1, city.lng + 0.1]
                ];
                
                L.imageOverlay(data.url, imageBounds, {
                    opacity: 0.7,
                    attribution: 'NASA Earth Observatory'
                }).addTo(map);
            }
        })
        .catch(error => {
            console.log('NASA imagery not available, using base map');
        });
}

// Add custom map controls
function addMapControls() {
    // Add layer control
    const layerControl = L.control.layers(null, null, {
        position: 'topright'
    }).addTo(map);

    // Add scale control
    L.control.scale({
        position: 'bottomleft'
    }).addTo(map);
}

// Setup event listeners
function setupEventListeners() {
    // Layer checkboxes
    document.getElementById('heatLayer').addEventListener('change', toggleHeatLayer);
    document.getElementById('airQualityLayer').addEventListener('change', toggleAirQualityLayer);
    document.getElementById('floodLayer').addEventListener('change', toggleFloodLayer);
    document.getElementById('greenLayer').addEventListener('change', toggleGreenLayer);
    document.getElementById('growthLayer').addEventListener('change', toggleGrowthLayer);

    // Map click events
    map.on('click', function(e) {
        showLocationData(e.latlng);
    });
}

// Load initial data
async function loadInitialData() {
    showLoading(true);
    
    try {
        const city = CITIES[currentCity];
        
        // Load all data layers in parallel
        await Promise.all([
            loadHeatData(city.lat, city.lng),
            loadAirQualityData(city.lat, city.lng),
            loadGreenSpaceData(city.lat, city.lng),
            loadWaterStressData(city.lat, city.lng)
        ]);
        
        updateMetrics();
        showLoading(false);
    } catch (error) {
        console.error('Error loading initial data:', error);
        showLoading(false);
        // Use mock data if API fails
        loadMockData();
    }
}

// NASA API Functions (via Backend)
async function fetchNASAEarthImagery(lat, lng) {
    const url = `${BACKEND_URL}/api/nasa/imagery?lat=${lat}&lng=${lng}&dim=0.1`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Backend API error');
        return await response.json();
    } catch (error) {
        console.log('Backend API error:', error);
        return null;
    }
}

async function fetchNASAAirQuality(lat, lng) {
    // For now, use mock data (can be replaced with real API later)
    return generateMockAirQuality(lat, lng);
}

// Data loading functions
async function loadHeatData(lat, lng) {
    // Simulate heat island data based on urban density
    const heatData = generateHeatIslandData(lat, lng);
    
    if (dataLayers.heat) {
        map.removeLayer(dataLayers.heat);
    }
    
    dataLayers.heat = L.heatLayer(heatData, {
        radius: 25,
        blur: 15,
        maxZoom: 17,
        max: 1,
        gradient: {
            0.0: 'blue',
            0.2: 'cyan',
            0.4: 'lime',
            0.6: 'yellow',
            0.8: 'orange',
            1.0: 'red'
        }
    });
    
    if (document.getElementById('heatLayer').checked) {
        dataLayers.heat.addTo(map);
    }
    
    return heatData;
}

async function loadAirQualityData(lat, lng) {
    const airQualityData = await fetchNASAAirQuality(lat, lng);
    
    if (dataLayers.airQuality) {
        map.removeLayer(dataLayers.airQuality);
    }
    
    // Create air quality markers
    const markers = createAirQualityMarkers(lat, lng, airQualityData);
    dataLayers.airQuality = L.layerGroup(markers);
    
    if (document.getElementById('airQualityLayer').checked) {
        dataLayers.airQuality.addTo(map);
    }
    
    return airQualityData;
}

async function loadGreenSpaceData(lat, lng) {
    const greenData = generateGreenSpaceData(lat, lng);
    
    if (dataLayers.green) {
        map.removeLayer(dataLayers.green);
    }
    
    // Create green space polygons
    const polygons = createGreenSpacePolygons(lat, lng, greenData);
    dataLayers.green = L.layerGroup(polygons);
    
    if (document.getElementById('greenLayer').checked) {
        dataLayers.green.addTo(map);
    }
    
    return greenData;
}

async function loadWaterStressData(lat, lng) {
    const waterData = generateWaterStressData(lat, lng);
    
    // Update water stress metric
    document.getElementById('waterValue').textContent = `${waterData.stressLevel}%`;
    document.getElementById('waterTrend').textContent = waterData.trend;
    
    return waterData;
}

// Mock data generation functions
function generateHeatIslandData(lat, lng) {
    const heatPoints = [];
    const numPoints = 50;
    
    for (let i = 0; i < numPoints; i++) {
        const offsetLat = (Math.random() - 0.5) * 0.2;
        const offsetLng = (Math.random() - 0.5) * 0.2;
        const intensity = Math.random();
        
        heatPoints.push([lat + offsetLat, lng + offsetLng, intensity]);
    }
    
    return heatPoints;
}

function generateMockAirQuality(lat, lng) {
    return {
        aqi: Math.floor(Math.random() * 200) + 50,
        pollutants: {
            pm25: Math.random() * 50,
            pm10: Math.random() * 80,
            no2: Math.random() * 100,
            o3: Math.random() * 60
        },
        timestamp: new Date().toISOString()
    };
}

function generateGreenSpaceData(lat, lng) {
    return {
        coverage: Math.floor(Math.random() * 40) + 20,
        parks: Math.floor(Math.random() * 15) + 5,
        trees: Math.floor(Math.random() * 10000) + 5000,
        trend: Math.random() > 0.5 ? 'increasing' : 'decreasing'
    };
}

function generateWaterStressData(lat, lng) {
    return {
        stressLevel: Math.floor(Math.random() * 80) + 20,
        trend: Math.random() > 0.5 ? 'improving' : 'declining',
        floodRisk: Math.random() > 0.7 ? 'high' : 'medium'
    };
}

function createAirQualityMarkers(lat, lng, data) {
    const markers = [];
    const numStations = 8;
    
    for (let i = 0; i < numStations; i++) {
        const offsetLat = (Math.random() - 0.5) * 0.15;
        const offsetLng = (Math.random() - 0.5) * 0.15;
        const aqi = Math.floor(Math.random() * 200) + 50;
        
        const color = getAQIColor(aqi);
        
        const marker = L.circleMarker([lat + offsetLat, lng + offsetLng], {
            radius: 8,
            fillColor: color,
            color: 'white',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).bindPopup(`
            <div style="text-align: center;">
                <h4>Air Quality Station</h4>
                <p><strong>AQI:</strong> ${aqi}</p>
                <p><strong>Status:</strong> ${getAQIStatus(aqi)}</p>
                <p><strong>PM2.5:</strong> ${Math.floor(Math.random() * 50)} μg/m³</p>
            </div>
        `);
        
        markers.push(marker);
    }
    
    return markers;
}

function createGreenSpacePolygons(lat, lng, data) {
    const polygons = [];
    const numParks = 6;
    
    for (let i = 0; i < numParks; i++) {
        const centerLat = lat + (Math.random() - 0.5) * 0.1;
        const centerLng = lng + (Math.random() - 0.5) * 0.1;
        
        const parkBounds = [
            [centerLat - 0.02, centerLng - 0.02],
            [centerLat + 0.02, centerLng + 0.02]
        ];
        
        const polygon = L.rectangle(parkBounds, {
            color: '#10b981',
            fillColor: '#10b981',
            fillOpacity: 0.3,
            weight: 2
        }).bindPopup(`
            <div style="text-align: center;">
                <h4>Green Space</h4>
                <p><strong>Type:</strong> Urban Park</p>
                <p><strong>Size:</strong> ${Math.floor(Math.random() * 50) + 10} hectares</p>
                <p><strong>Vegetation:</strong> ${Math.floor(Math.random() * 80) + 20}%</p>
            </div>
        `);
        
        polygons.push(polygon);
    }
    
    return polygons;
}

// Utility functions
function getAQIColor(aqi) {
    if (aqi <= 50) return '#00e400';
    if (aqi <= 100) return '#ffff00';
    if (aqi <= 150) return '#ff7e00';
    if (aqi <= 200) return '#ff0000';
    return '#8f3f97';
}

function getAQIStatus(aqi) {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
    if (aqi <= 200) return 'Unhealthy';
    return 'Very Unhealthy';
}

// Layer toggle functions
function toggleHeatLayer() {
    if (document.getElementById('heatLayer').checked) {
        if (dataLayers.heat) {
            dataLayers.heat.addTo(map);
        }
    } else {
        if (dataLayers.heat) {
            map.removeLayer(dataLayers.heat);
        }
    }
}

function toggleAirQualityLayer() {
    if (document.getElementById('airQualityLayer').checked) {
        if (dataLayers.airQuality) {
            dataLayers.airQuality.addTo(map);
        }
    } else {
        if (dataLayers.airQuality) {
            map.removeLayer(dataLayers.airQuality);
        }
    }
}

function toggleFloodLayer() {
    if (document.getElementById('floodLayer').checked) {
        // Add flood risk visualization
        addFloodRiskLayer();
    } else {
        if (dataLayers.flood) {
            map.removeLayer(dataLayers.flood);
        }
    }
}

function toggleGreenLayer() {
    if (document.getElementById('greenLayer').checked) {
        if (dataLayers.green) {
            dataLayers.green.addTo(map);
        }
    } else {
        if (dataLayers.green) {
            map.removeLayer(dataLayers.green);
        }
    }
}

function toggleGrowthLayer() {
    if (document.getElementById('growthLayer').checked) {
        // Add urban growth visualization
        addUrbanGrowthLayer();
    } else {
        if (dataLayers.growth) {
            map.removeLayer(dataLayers.growth);
        }
    }
}

// Scenario simulation functions
function simulateTreePlanting() {
    showLoading(true);
    
    setTimeout(() => {
        // Simulate the effect of adding trees
        const currentHeat = document.getElementById('heatValue').textContent;
        const currentGreen = document.getElementById('greenValue').textContent;
        
        const newHeat = parseInt(currentHeat) - 2;
        const newGreen = parseInt(currentGreen) + 15;
        
        document.getElementById('heatValue').textContent = `${newHeat}°C`;
        document.getElementById('greenValue').textContent = `${newGreen}%`;
        document.getElementById('heatTrend').textContent = 'improving';
        document.getElementById('greenTrend').textContent = 'increasing';
        
        // Add visual feedback
        showScenarioResult('Tree Planting Simulation', 
            `Added green corridor reduced heat by 2°C and increased green coverage by 15%`);
        
        showLoading(false);
    }, 2000);
}

function simulateCoolRoofs() {
    showLoading(true);
    
    setTimeout(() => {
        const currentHeat = document.getElementById('heatValue').textContent;
        const currentAir = document.getElementById('airValue').textContent;
        
        const newHeat = parseInt(currentHeat) - 3;
        const newAir = parseInt(currentAir) - 20;
        
        document.getElementById('heatValue').textContent = `${newHeat}°C`;
        document.getElementById('airValue').textContent = `${newAir} AQI`;
        document.getElementById('heatTrend').textContent = 'improving';
        document.getElementById('airTrend').textContent = 'improving';
        
        showScenarioResult('Cool Roofs Simulation', 
            `Installing reflective roofs reduced heat by 3°C and improved air quality by 20 AQI points`);
        
        showLoading(false);
    }, 2000);
}

function simulateFloodMitigation() {
    showLoading(true);
    
    setTimeout(() => {
        const currentWater = document.getElementById('waterValue').textContent;
        const newWater = parseInt(currentWater) - 25;
        
        document.getElementById('waterValue').textContent = `${newWater}%`;
        document.getElementById('waterTrend').textContent = 'improving';
        
        showScenarioResult('Flood Mitigation Simulation', 
            `Green infrastructure reduced water stress by 25% and flood risk significantly`);
        
        showLoading(false);
    }, 2000);
}

// Additional layer functions
function addFloodRiskLayer() {
    const city = CITIES[currentCity];
    const floodData = generateFloodRiskData(city.lat, city.lng);
    
    if (dataLayers.flood) {
        map.removeLayer(dataLayers.flood);
    }
    
    const floodPolygons = createFloodRiskPolygons(city.lat, city.lng, floodData);
    dataLayers.flood = L.layerGroup(floodPolygons);
    dataLayers.flood.addTo(map);
}

function addUrbanGrowthLayer() {
    const city = CITIES[currentCity];
    const growthData = generateUrbanGrowthData(city.lat, city.lng);
    
    if (dataLayers.growth) {
        map.removeLayer(dataLayers.growth);
    }
    
    const growthMarkers = createUrbanGrowthMarkers(city.lat, city.lng, growthData);
    dataLayers.growth = L.layerGroup(growthMarkers);
    dataLayers.growth.addTo(map);
}

// Data generation for additional layers
function generateFloodRiskData(lat, lng) {
    return {
        highRisk: Math.floor(Math.random() * 5) + 3,
        mediumRisk: Math.floor(Math.random() * 8) + 5,
        lowRisk: Math.floor(Math.random() * 10) + 8
    };
}

function generateUrbanGrowthData(lat, lng) {
    return {
        newHousing: Math.floor(Math.random() * 15) + 5,
        commercial: Math.floor(Math.random() * 10) + 3,
        infrastructure: Math.floor(Math.random() * 8) + 2
    };
}

function createFloodRiskPolygons(lat, lng, data) {
    const polygons = [];
    
    // High risk areas
    for (let i = 0; i < data.highRisk; i++) {
        const centerLat = lat + (Math.random() - 0.5) * 0.1;
        const centerLng = lng + (Math.random() - 0.5) * 0.1;
        
        const bounds = [
            [centerLat - 0.01, centerLng - 0.01],
            [centerLat + 0.01, centerLng + 0.01]
        ];
        
        const polygon = L.rectangle(bounds, {
            color: '#dc2626',
            fillColor: '#dc2626',
            fillOpacity: 0.4,
            weight: 2
        }).bindPopup('<strong>High Flood Risk</strong><br>Requires immediate attention');
        
        polygons.push(polygon);
    }
    
    return polygons;
}

function createUrbanGrowthMarkers(lat, lng, data) {
    const markers = [];
    
    // New housing developments
    for (let i = 0; i < data.newHousing; i++) {
        const offsetLat = (Math.random() - 0.5) * 0.1;
        const offsetLng = (Math.random() - 0.5) * 0.1;
        
        const marker = L.marker([lat + offsetLat, lng + offsetLng], {
            icon: L.divIcon({
                className: 'growth-marker',
                html: '<i class="fas fa-home" style="color: #3b82f6; font-size: 16px;"></i>',
                iconSize: [20, 20]
            })
        }).bindPopup('<strong>New Housing Development</strong><br>Under construction');
        
        markers.push(marker);
    }
    
    return markers;
}

// Utility functions
function changeCity() {
    const selectedCity = document.getElementById('citySelect').value;
    currentCity = selectedCity;
    
    const city = CITIES[currentCity];
    map.setView([city.lat, city.lng], 12);
    
    // Reload data for new city
    loadInitialData();
}

function refreshData() {
    loadInitialData();
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

function showLocationData(latlng) {
    const popup = L.popup()
        .setLatLng(latlng)
        .setContent(`
            <div style="text-align: center;">
                <h4>Location Analysis</h4>
                <p><strong>Coordinates:</strong> ${latlng.lat.toFixed(4)}, ${latlng.lng.toFixed(4)}</p>
                <p><strong>Heat Index:</strong> ${Math.floor(Math.random() * 10) + 25}°C</p>
                <p><strong>Air Quality:</strong> ${Math.floor(Math.random() * 100) + 50} AQI</p>
                <p><strong>Green Coverage:</strong> ${Math.floor(Math.random() * 50) + 20}%</p>
            </div>
        `)
        .openOn(map);
}

function showScenarioResult(title, message) {
    const popup = L.popup()
        .setLatLng(map.getCenter())
        .setContent(`
            <div style="text-align: center;">
                <h4 style="color: #10b981;">${title}</h4>
                <p>${message}</p>
                <div style="margin-top: 10px;">
                    <i class="fas fa-check-circle" style="color: #10b981; font-size: 24px;"></i>
                </div>
            </div>
        `)
        .openOn(map);
    
    // Auto-close after 5 seconds
    setTimeout(() => {
        map.closePopup();
    }, 5000);
}

function updateMetrics() {
    // Update status panel
    document.getElementById('heatIndex').textContent = `${Math.floor(Math.random() * 10) + 25}°C`;
    document.getElementById('airQuality').textContent = `${Math.floor(Math.random() * 100) + 50} AQI`;
    document.getElementById('greenCoverage').textContent = `${Math.floor(Math.random() * 50) + 20}%`;
    
    // Update metric cards
    document.getElementById('heatValue').textContent = `${Math.floor(Math.random() * 10) + 25}°C`;
    document.getElementById('airValue').textContent = `${Math.floor(Math.random() * 100) + 50} AQI`;
    document.getElementById('waterValue').textContent = `${Math.floor(Math.random() * 80) + 20}%`;
    document.getElementById('greenValue').textContent = `${Math.floor(Math.random() * 50) + 20}%`;
    
    // Update trends
    const trends = ['improving', 'declining', 'stable'];
    document.getElementById('heatTrend').textContent = trends[Math.floor(Math.random() * 3)];
    document.getElementById('airTrend').textContent = trends[Math.floor(Math.random() * 3)];
    document.getElementById('waterTrend').textContent = trends[Math.floor(Math.random() * 3)];
    document.getElementById('greenTrend').textContent = trends[Math.floor(Math.random() * 3)];
}

function loadMockData() {
    // Fallback to mock data if NASA APIs are unavailable
    updateMetrics();
    console.log('Using mock data - NASA APIs may be unavailable');
}

// Initialize base map layers
function initializeBaseLayers() {
    // Satellite layer (default)
    baseLayers.satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '© Esri, Maxar, GeoEye, Earthstar Geographics, CNES/Airbus DS, USDA, USGS, AeroGRID, IGN, and the GIS User Community'
    });

    // Topographic layer
    baseLayers.topographic = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenTopoMap contributors'
    });

    // Terrain layer
    baseLayers.terrain = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: '© Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
    });

    // Street layer
    baseLayers.streets = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    });
}

// Change base layer
function changeBaseLayer(layerType) {
    // Remove all base layers
    Object.values(baseLayers).forEach(layer => {
        if (map.hasLayer(layer)) {
            map.removeLayer(layer);
        }
    });

    // Add selected layer
    if (baseLayers[layerType]) {
        baseLayers[layerType].addTo(map);
    }
}

// Search location functionality
function searchLocation() {
    const searchInput = document.getElementById('locationSearch').value.trim();
    
    if (!searchInput) {
        alert('Please enter coordinates or place name');
        return;
    }

    // Try to parse coordinates
    const coordPattern = /^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$/;
    const match = searchInput.match(coordPattern);
    
    if (match) {
        const lat = parseFloat(match[1]);
        const lng = parseFloat(match[2]);
        
        if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
            goToLocation(lat, lng, `Custom Location (${lat.toFixed(4)}, ${lng.toFixed(4)})`);
            return;
        }
    }

    // Try to find city by name
    const foundCity = Object.entries(CITIES).find(([key, city]) => 
        city.name.toLowerCase().includes(searchInput.toLowerCase())
    );

    if (foundCity) {
        const [key, city] = foundCity;
        document.getElementById('citySelect').value = key;
        changeCity();
        return;
    }

    // Use geocoding for other locations
    geocodeLocation(searchInput);
}

// Geocode location using Nominatim
async function geocodeLocation(query) {
    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`);
        const data = await response.json();
        
        if (data.length > 0) {
            const result = data[0];
            const lat = parseFloat(result.lat);
            const lng = parseFloat(result.lon);
            goToLocation(lat, lng, result.display_name);
        } else {
            alert('Location not found. Please try a different search term or use coordinates (lat, lng)');
        }
    } catch (error) {
        console.error('Geocoding error:', error);
        alert('Error searching location. Please try again.');
    }
}

// Go to specific location
function goToLocation(lat, lng, name) {
    map.setView([lat, lng], 12);
    
    // Add a marker for the location
    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(`
        <div style="text-align: center;">
            <h4>${name}</h4>
            <p><strong>Coordinates:</strong> ${lat.toFixed(4)}, ${lng.toFixed(4)}</p>
        </div>
    `).openPopup();
    
    // Clear search input
    document.getElementById('locationSearch').value = '';
    
    // Show success message
    showNotification(`Navigated to ${name}`, 'success');
}

// Show elevation profile
function showElevationProfile() {
    if (elevationProfile) {
        map.removeLayer(elevationProfile);
    }
    
    const city = CITIES[currentCity];
    const elevationData = generateElevationData(city.lat, city.lng);
    
    elevationProfile = L.layerGroup();
    
    // Add elevation markers
    elevationData.forEach(point => {
        const marker = L.circleMarker([point.lat, point.lng], {
            radius: 6,
            fillColor: getElevationColor(point.elevation),
            color: 'white',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).bindPopup(`
            <div style="text-align: center;">
                <h4>Elevation Point</h4>
                <p><strong>Elevation:</strong> ${point.elevation}m</p>
                <p><strong>Coordinates:</strong> ${point.lat.toFixed(4)}, ${point.lng.toFixed(4)}</p>
            </div>
        `);
        
        elevationProfile.addLayer(marker);
    });
    
    elevationProfile.addTo(map);
    
    // Update elevation info
    document.getElementById('elevationInfo').innerHTML = `
        <h4>Elevation Analysis</h4>
        <p><strong>Highest Point:</strong> ${Math.max(...elevationData.map(p => p.elevation))}m</p>
        <p><strong>Lowest Point:</strong> ${Math.min(...elevationData.map(p => p.elevation))}m</p>
        <p><strong>Average:</strong> ${Math.round(elevationData.reduce((sum, p) => sum + p.elevation, 0) / elevationData.length)}m</p>
        <p><strong>Total Points:</strong> ${elevationData.length}</p>
    `;
    
    showNotification('Elevation profile loaded', 'success');
}

// Toggle contour lines
function toggleContourLines() {
    if (contourLayer) {
        map.removeLayer(contourLayer);
        contourLayer = null;
        showNotification('Contour lines hidden', 'info');
    } else {
        const city = CITIES[currentCity];
        const contourData = generateContourData(city.lat, city.lng);
        
        contourLayer = L.layerGroup();
        
        // Add contour lines
        contourData.forEach(contour => {
            const polyline = L.polyline(contour.coordinates, {
                color: contour.color,
                weight: 2,
                opacity: 0.8
            }).bindPopup(`
                <div style="text-align: center;">
                    <h4>Contour Line</h4>
                    <p><strong>Elevation:</strong> ${contour.elevation}m</p>
                </div>
            `);
            
            contourLayer.addLayer(polyline);
        });
        
        contourLayer.addTo(map);
        showNotification('Contour lines displayed', 'success');
    }
}

// Generate elevation data
function generateElevationData(lat, lng) {
    const points = [];
    const numPoints = 25;
    
    for (let i = 0; i < numPoints; i++) {
        const offsetLat = (Math.random() - 0.5) * 0.1;
        const offsetLng = (Math.random() - 0.5) * 0.1;
        const elevation = Math.floor(Math.random() * 200) + 50; // 50-250m elevation
        
        points.push({
            lat: lat + offsetLat,
            lng: lng + offsetLng,
            elevation: elevation
        });
    }
    
    return points;
}

// Generate contour data
function generateContourData(lat, lng) {
    const contours = [];
    const elevations = [50, 75, 100, 125, 150, 175, 200, 225, 250];
    
    elevations.forEach(elevation => {
        const contour = {
            elevation: elevation,
            coordinates: [],
            color: getElevationColor(elevation)
        };
        
        // Generate contour line coordinates (simplified)
        const numPoints = 20;
        for (let i = 0; i < numPoints; i++) {
            const angle = (i / numPoints) * 2 * Math.PI;
            const radius = 0.02 + Math.random() * 0.01;
            const pointLat = lat + radius * Math.cos(angle);
            const pointLng = lng + radius * Math.sin(angle);
            
            contour.coordinates.push([pointLat, pointLng]);
        }
        
        contours.push(contour);
    });
    
    return contours;
}

// Get elevation color
function getElevationColor(elevation) {
    if (elevation < 100) return '#0066cc';
    if (elevation < 150) return '#00cc66';
    if (elevation < 200) return '#ffcc00';
    if (elevation < 250) return '#ff6600';
    return '#cc0000';
}

// AI Chat Functions
async function sendAIMessage() {
    const input = document.getElementById('aiChatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Show loading indicator
    const loadingMsg = addChatMessage('Thinking...', 'ai');
    
    try {
        // Call backend AI endpoint
        const response = await fetch(`${BACKEND_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                selectedAreaData: selectedAreaData,
                sessionId: 'default'
            })
        });
        
        if (!response.ok) throw new Error('Backend API error');
        
        const data = await response.json();
        
        // Remove loading message
        loadingMsg.remove();
        
        // Add AI response
        addChatMessage(data.response, 'ai');
    } catch (error) {
        console.error('Error calling AI:', error);
        loadingMsg.remove();
        addChatMessage('Sorry, I\'m having trouble connecting. Please try again.', 'ai');
    }
}

function askAI(question) {
    document.getElementById('aiChatInput').value = question;
    sendAIMessage();
}

function addChatMessage(content, sender) {
    const chatMessages = document.getElementById('aiChatMessages');
    const messageDiv = document.createElement('div');
    
    if (sender === 'user') {
        messageDiv.className = 'user-message';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${content}</p>
                <small>User</small>
            </div>
        `;
    } else {
        messageDiv.className = 'ai-message';
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p>${content}</p>
                <small>AI Assistant</small>
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;  // Return for removal if needed
}

function generateAIResponse(question) {
    let response = '';
    
    // Check if we have selected area data for context-aware responses
    if (selectedAreaData) {
        response = generateContextualResponse(question, selectedAreaData);
    } else {
        response = generateGeneralResponse(question);
    }
    
    return response;
}

function generateContextualResponse(question, areaData) {
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes('green infrastructure')) {
        return `Based on the selected area (${areaData.area} km²), I recommend focusing green infrastructure where heat islands are strongest. With ${areaData.greenCoverage}% current coverage, target areas with heat index above ${areaData.heatIndex}°C. Consider: 1) Tree corridors along major roads, 2) Green roofs on ${areaData.buildings} buildings, 3) Urban parks in low-coverage zones.`;
    }
    
    if (lowerQuestion.includes('heat islands')) {
        return `For the selected area with ${areaData.heatIndex}°C heat index and ${areaData.population.toLocaleString()} residents, I suggest: 1) Increase tree canopy by ${Math.max(0, 30 - areaData.greenCoverage)}%, 2) Install cool roofs on high-density buildings, 3) Create green corridors, 4) Add water features in heat hotspots. Priority: Focus on areas with highest building density.`;
    }
    
    if (lowerQuestion.includes('flood mitigation')) {
        return `Given the ${areaData.floodRisk} flood risk in this ${areaData.area} km² area, prioritize: 1) Green infrastructure in flood-prone zones, 2) Permeable pavements for ${areaData.buildings} buildings, 3) Bioswales along drainage paths, 4) Retention ponds in low-lying areas. Focus on protecting ${areaData.population.toLocaleString()} residents from flood risks.`;
    }
    
    if (lowerQuestion.includes('air quality')) {
        return `With ${areaData.airQuality} AQI in the selected area, implement: 1) Low-emission zones around industrial areas, 2) Green barriers along major roads, 3) Urban forest development to improve air quality for ${areaData.population.toLocaleString()} residents, 4) Electric vehicle infrastructure. Target reduction to AQI < 100.`;
    }
    
    if (lowerQuestion.includes('urban planning')) {
        return `For sustainable development in this ${areaData.area} km² area with ${areaData.population.toLocaleString()} residents: 1) Mixed-use development near transport hubs, 2) Green transportation networks, 3) Climate-resilient infrastructure for ${areaData.floodRisk} flood risk, 4) Smart growth strategies balancing heat mitigation (${areaData.heatIndex}°C) with green space (${areaData.greenCoverage}%).`;
    }
    
    return `I'm analyzing the selected area (${areaData.area} km²) with ${areaData.population.toLocaleString()} residents. Current metrics: ${areaData.heatIndex}°C heat, ${areaData.airQuality} AQI, ${areaData.greenCoverage}% green coverage. What specific aspect would you like me to focus on?`;
}

function generateGeneralResponse(question) {
    const responses = {
        'green infrastructure': 'Based on the current data, I recommend focusing green infrastructure in areas with high heat island effects and low green coverage. Consider tree corridors along major roads and green roofs on commercial buildings.',
        'heat islands': 'To reduce urban heat islands, I suggest: 1) Increasing tree canopy coverage by 30%, 2) Installing cool/reflective roofs, 3) Creating green corridors, and 4) Implementing water features in dense urban areas.',
        'flood mitigation': 'For flood mitigation, focus on low-lying areas identified in the flood risk layer. Implement green infrastructure like bioswales, permeable pavements, and retention ponds in high-risk zones.',
        'air quality': 'To improve air quality, consider: 1) Low-emission zones in industrial areas, 2) Green barriers along major roads, 3) Urban forest development, and 4) Transitioning to electric public transport.',
        'urban planning': 'For sustainable urban development, integrate environmental data with population growth projections. Prioritize mixed-use development, green transportation networks, and climate-resilient infrastructure.',
        'default': 'I can help you analyze environmental data and suggest planning strategies. Try asking about specific topics like green infrastructure, heat islands, flood mitigation, or air quality improvements. You can also select a specific area on the map for targeted analysis.'
    };
    
    const lowerQuestion = question.toLowerCase();
    
    for (const [key, response] of Object.entries(responses)) {
        if (lowerQuestion.includes(key)) {
            return response;
        }
    }
    
    return responses.default;
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 10000;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Area Selection Functions
function enableAreaSelection() {
    if (selectionMode) {
        disableAreaSelection();
        showNotification('Area selection cancelled', 'info');
        return;
    }
    
    selectionMode = true;
    document.getElementById('selectAreaBtn').classList.add('active');
    document.getElementById('selectAreaBtn').innerHTML = '<i class="fas fa-stop"></i> Cancel Selection';
    
    // Change cursor to indicate selection mode
    document.getElementById('map').style.cursor = 'crosshair';
    
    // Add click event for area selection
    map.on('click', handleAreaSelection);
    
    showNotification('Click and drag to select an area on the map', 'info');
}

function disableAreaSelection() {
    selectionMode = false;
    document.getElementById('selectAreaBtn').classList.remove('active');
    document.getElementById('selectAreaBtn').innerHTML = '<i class="fas fa-vector-square"></i> Select Area';
    
    // Reset cursor
    document.getElementById('map').style.cursor = '';
    
    // Re-enable map dragging
    map.dragging.enable();
    
    // Remove click event
    map.off('click', handleAreaSelection);
}

function handleAreaSelection(e) {
    if (!selectionMode) return;
    
    // Prevent default map dragging
    e.originalEvent.preventDefault();
    e.originalEvent.stopPropagation();
    
    const startPoint = e.latlng;
    let endPoint = null;
    let rectangle = null;
    
    // Disable map dragging during selection
    map.dragging.disable();
    
    // Create temporary rectangle
    const createRectangle = (endLatLng) => {
        if (rectangle) {
            map.removeLayer(rectangle);
        }
        
        const bounds = L.latLngBounds(startPoint, endLatLng);
        rectangle = L.rectangle(bounds, {
            color: '#3b82f6',
            fillColor: '#3b82f6',
            fillOpacity: 0.2,
            weight: 3,
            dashArray: '5, 5'
        }).addTo(map);
        
        return rectangle;
    };
    
    // Handle mouse move to show preview
    const onMouseMove = (e) => {
        e.originalEvent.preventDefault();
        e.originalEvent.stopPropagation();
        endPoint = e.latlng;
        createRectangle(endPoint);
    };
    
    // Handle mouse up to finalize selection
    const onMouseUp = (e) => {
        e.originalEvent.preventDefault();
        e.originalEvent.stopPropagation();
        
        endPoint = e.latlng;
        
        // Re-enable map dragging
        map.dragging.enable();
        
        // Remove event listeners
        map.off('mousemove', onMouseMove);
        map.off('mouseup', onMouseUp);
        
        // Create final rectangle
        if (rectangle) {
            map.removeLayer(rectangle);
        }
        
        const bounds = L.latLngBounds(startPoint, endPoint);
        selectionRectangle = L.rectangle(bounds, {
            color: '#10b981',
            fillColor: '#10b981',
            fillOpacity: 0.3,
            weight: 3
        }).addTo(map);
        
        // Bind popup with area info
        const area = calculateArea(bounds);
        selectionRectangle.bindPopup(`
            <div style="text-align: center;">
                <h4>Selected Area</h4>
                <p><strong>Area:</strong> ${area.area} km²</p>
                <p><strong>Perimeter:</strong> ${area.perimeter} km</p>
                <p><strong>Center:</strong> ${bounds.getCenter().lat.toFixed(4)}, ${bounds.getCenter().lng.toFixed(4)}</p>
            </div>
        `);
        
        // Store selected area data
        selectedArea = {
            bounds: bounds,
            center: bounds.getCenter(),
            area: area.area,
            perimeter: area.perimeter
        };
        
        // Generate data for selected area
        selectedAreaData = generateAreaData(bounds);
        
        // Update UI
        updateSelectionInfo();
        showSelectionControls();
        
        // Disable selection mode
        disableAreaSelection();
        
        showNotification('Area selected successfully! Click "Focus on Area" to analyze', 'success');
    };
    
    // Add event listeners
    map.on('mousemove', onMouseMove);
    map.on('mouseup', onMouseUp);
}

function calculateArea(bounds) {
    const latDiff = Math.abs(bounds.getNorth() - bounds.getSouth());
    const lngDiff = Math.abs(bounds.getEast() - bounds.getWest());
    
    // Approximate calculation (more accurate would require spherical geometry)
    const latKm = latDiff * 111; // 1 degree latitude ≈ 111 km
    const lngKm = lngDiff * 111 * Math.cos(bounds.getCenter().lat * Math.PI / 180);
    
    const area = (latKm * lngKm).toFixed(2);
    const perimeter = (2 * (latKm + lngKm)).toFixed(2);
    
    return { area, perimeter };
}

function generateAreaData(bounds) {
    const center = bounds.getCenter();
    const area = calculateArea(bounds);
    
    return {
        bounds: bounds,
        center: center,
        area: area.area,
        perimeter: area.perimeter,
        heatIndex: Math.floor(Math.random() * 15) + 25, // 25-40°C
        airQuality: Math.floor(Math.random() * 150) + 50, // 50-200 AQI
        greenCoverage: Math.floor(Math.random() * 60) + 10, // 10-70%
        waterStress: Math.floor(Math.random() * 80) + 20, // 20-100%
        elevation: {
            min: Math.floor(Math.random() * 100) + 10,
            max: Math.floor(Math.random() * 200) + 150,
            avg: Math.floor(Math.random() * 100) + 75
        },
        floodRisk: Math.random() > 0.5 ? 'High' : 'Medium',
        population: Math.floor(Math.random() * 50000) + 5000,
        buildings: Math.floor(Math.random() * 1000) + 100
    };
}

function updateSelectionInfo() {
    if (!selectedArea || !selectedAreaData) return;
    
    const info = document.getElementById('selectionInfo');
    info.innerHTML = `
        <h4>Selected Area Analysis</h4>
        <div class="area-stats">
            <div class="stat-item">
                <span>Area:</span>
                <span class="stat-value">${selectedArea.area} km²</span>
            </div>
            <div class="stat-item">
                <span>Population:</span>
                <span class="stat-value">${selectedAreaData.population.toLocaleString()}</span>
            </div>
            <div class="stat-item">
                <span>Heat Index:</span>
                <span class="stat-value">${selectedAreaData.heatIndex}°C</span>
            </div>
            <div class="stat-item">
                <span>Air Quality:</span>
                <span class="stat-value">${selectedAreaData.airQuality} AQI</span>
            </div>
            <div class="stat-item">
                <span>Green Coverage:</span>
                <span class="stat-value">${selectedAreaData.greenCoverage}%</span>
            </div>
            <div class="stat-item">
                <span>Flood Risk:</span>
                <span class="stat-value">${selectedAreaData.floodRisk}</span>
            </div>
        </div>
    `;
}

function showSelectionControls() {
    document.getElementById('clearSelectionBtn').style.display = 'block';
    document.getElementById('focusBtn').style.display = 'block';
    document.getElementById('analyzeAreaBtn').style.display = 'block';
}

function clearSelection() {
    if (selectionRectangle) {
        map.removeLayer(selectionRectangle);
        selectionRectangle = null;
    }
    
    selectedArea = null;
    selectedAreaData = null;
    
    // Hide controls
    document.getElementById('clearSelectionBtn').style.display = 'none';
    document.getElementById('focusBtn').style.display = 'none';
    document.getElementById('analyzeAreaBtn').style.display = 'none';
    
    // Reset info
    document.getElementById('selectionInfo').innerHTML = '<p>Click "Select Area" to draw a focus region</p>';
    
    showNotification('Selection cleared', 'info');
}

function focusOnSelection() {
    if (!selectedArea) return;
    
    // Zoom to selected area
    map.fitBounds(selectedArea.bounds, { padding: [20, 20] });
    
    // Update metrics to show area-specific data
    document.getElementById('heatValue').textContent = `${selectedAreaData.heatIndex}°C`;
    document.getElementById('airValue').textContent = `${selectedAreaData.airQuality} AQI`;
    document.getElementById('greenValue').textContent = `${selectedAreaData.greenCoverage}%`;
    document.getElementById('waterValue').textContent = `${selectedAreaData.waterStress}%`;
    
    // Update trends based on area data
    document.getElementById('heatTrend').textContent = selectedAreaData.heatIndex > 30 ? 'high' : 'moderate';
    document.getElementById('airTrend').textContent = selectedAreaData.airQuality > 100 ? 'poor' : 'good';
    document.getElementById('greenTrend').textContent = selectedAreaData.greenCoverage > 30 ? 'good' : 'needs improvement';
    document.getElementById('waterTrend').textContent = selectedAreaData.waterStress > 60 ? 'high stress' : 'moderate';
    
    showNotification('Focused on selected area - AI will now analyze this region', 'success');
}

async function analyzeSelectedArea() {
    if (!selectedAreaData) {
        showNotification('Please select an area first', 'error');
        return;
    }
    
    addChatMessage(`Analyzing selected area (${selectedArea.area} km²)...`, 'user');
    const loadingMsg = addChatMessage('Performing comprehensive analysis...', 'ai');
    
    try {
        // Call backend analysis endpoint
        const response = await fetch(`${BACKEND_URL}/api/analyze-area`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                areaData: selectedAreaData
            })
        });
        
        if (!response.ok) throw new Error('Backend API error');
        
        const data = await response.json();
        
        // Remove loading message
        loadingMsg.remove();
        
        // Add AI analysis
        addChatMessage(data.analysis, 'ai');
        
        showNotification('Analysis complete!', 'success');
    } catch (error) {
        console.error('Error analyzing area:', error);
        loadingMsg.remove();
        addChatMessage('Sorry, analysis failed. Please try again.', 'ai');
        showNotification('Analysis failed', 'error');
    }
}

function generateAreaAnalysis(data) {
    const issues = [];
    const recommendations = [];
    
    // Analyze heat
    if (data.heatIndex > 32) {
        issues.push('High heat stress detected');
        recommendations.push('Implement cooling strategies like green roofs and tree planting');
    }
    
    // Analyze air quality
    if (data.airQuality > 100) {
        issues.push('Poor air quality');
        recommendations.push('Create green barriers and reduce traffic emissions');
    }
    
    // Analyze green coverage
    if (data.greenCoverage < 25) {
        issues.push('Low green space coverage');
        recommendations.push('Increase urban green infrastructure and parks');
    }
    
    // Analyze flood risk
    if (data.floodRisk === 'High') {
        issues.push('High flood risk');
        recommendations.push('Implement flood mitigation systems and permeable surfaces');
    }
    
    let analysis = `## Area Analysis Report (${data.area} km²)\n\n`;
    analysis += `**Key Metrics:**\n`;
    analysis += `• Heat Index: ${data.heatIndex}°C\n`;
    analysis += `• Air Quality: ${data.airQuality} AQI\n`;
    analysis += `• Green Coverage: ${data.greenCoverage}%\n`;
    analysis += `• Water Stress: ${data.waterStress}%\n`;
    analysis += `• Population: ${data.population.toLocaleString()}\n\n`;
    
    if (issues.length > 0) {
        analysis += `**Identified Issues:**\n${issues.map(issue => `• ${issue}`).join('\n')}\n\n`;
    }
    
    if (recommendations.length > 0) {
        analysis += `**Recommendations:**\n${recommendations.map(rec => `• ${rec}`).join('\n')}\n\n`;
    }
    
    analysis += `**Priority Actions:**\n`;
    analysis += `1. Focus on ${data.heatIndex > 30 ? 'cooling infrastructure' : 'green space development'}\n`;
    analysis += `2. Address ${data.airQuality > 100 ? 'air quality concerns' : 'environmental monitoring'}\n`;
    analysis += `3. Plan for ${data.floodRisk === 'High' ? 'flood resilience' : 'sustainable development'}`;
    
    return analysis;
}

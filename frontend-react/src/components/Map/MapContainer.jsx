import { MapContainer as LeafletMap, TileLayer, useMap, useMapEvents, Marker, Popup, Circle, Polygon, Polyline } from 'react-leaflet'
import { useStore } from '../../store/useStore'
import { useEffect, memo, useState } from 'react'
import L from 'leaflet'
import { Crop } from 'lucide-react'
import StatusPanel from './StatusPanel'
import MapLegend from './MapLegend'
import './MapContainer.css'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'

// Component to update map view when center/zoom changes
const MapController = memo(function MapController() {
  const map = useMap()
  // Selective subscription - only subscribe to what we need
  const mapCenter = useStore((state) => state.mapCenter)
  const mapZoom = useStore((state) => state.mapZoom)
  const selectionMode = useStore((state) => state.selectionMode)

  useEffect(() => {
    if (mapCenter && mapZoom) {
      map.setView(mapCenter, mapZoom)
    }
  }, [mapCenter, mapZoom, map])

  // Apply cursor styles when selection mode changes
  useEffect(() => {
    const mapContainer = map.getContainer()
    if (mapContainer) {
      if (selectionMode) {
        mapContainer.style.cursor = 'crosshair'
        map.dragging.disable()
        map.doubleClickZoom.disable()
        map.scrollWheelZoom.disable()
        map.touchZoom.disable()
        map.boxZoom.disable()
        map.keyboard.disable()
      } else {
        mapContainer.style.cursor = 'default'
        map.dragging.enable()
        map.doubleClickZoom.enable()
        map.scrollWheelZoom.enable()
        map.touchZoom.enable()
        map.boxZoom.enable()
        map.keyboard.enable()
      }
    }
  }, [selectionMode, map])

  return null
})

// Heat Map Layer Component
const HeatMapLayer = memo(function HeatMapLayer() {
  const map = useMap()
  const layers = useStore((state) => state.layers)
  const mapCenter = useStore((state) => state.mapCenter)
  const selectedArea = useStore((state) => state.selectedArea)

  useEffect(() => {
    if (!layers.heat) return

    let heatData = []
    
    if (selectedArea && selectedArea.bounds) {
      // Generate heat data only within the selected area
      const bounds = selectedArea.bounds
      const minLat = Math.min(...bounds.map(point => point[0]))
      const maxLat = Math.max(...bounds.map(point => point[0]))
      const minLng = Math.min(...bounds.map(point => point[1]))
      const maxLng = Math.max(...bounds.map(point => point[1]))
      
      for (let i = 0; i < 30; i++) {
        const lat = minLat + Math.random() * (maxLat - minLat)
        const lng = minLng + Math.random() * (maxLng - minLng)
        const intensity = Math.random() * 100
        heatData.push([lat, lng, intensity])
      }
    } else {
      // Generate heat data around the current map center (full view)
      for (let i = 0; i < 50; i++) {
        const lat = mapCenter[0] + (Math.random() - 0.5) * 0.1
        const lng = mapCenter[1] + (Math.random() - 0.5) * 0.1
        const intensity = Math.random() * 100
        heatData.push([lat, lng, intensity])
      }
    }

    const heatLayer = L.heatLayer(heatData, {
      radius: 25,
      blur: 15,
      maxZoom: 17,
      gradient: {
        0.4: 'blue',
        0.6: 'cyan',
        0.7: 'lime',
        0.8: 'yellow',
        1.0: 'red'
      }
    })

    heatLayer.addTo(map)

    return () => {
      map.removeLayer(heatLayer)
    }
  }, [layers.heat, mapCenter, map, selectedArea])

  return null
})

// Air Quality Layer Component
const AirQualityLayer = memo(function AirQualityLayer() {
  const layers = useStore((state) => state.layers)
  const mapCenter = useStore((state) => state.mapCenter)
  const selectedArea = useStore((state) => state.selectedArea)

  if (!layers.airQuality) return null

  // Generate mock air quality data
  const airQualityData = []
  
  if (selectedArea && selectedArea.bounds) {
    // Generate air quality data only within the selected area
    const bounds = selectedArea.bounds
    const minLat = Math.min(...bounds.map(point => point[0]))
    const maxLat = Math.max(...bounds.map(point => point[0]))
    const minLng = Math.min(...bounds.map(point => point[1]))
    const maxLng = Math.max(...bounds.map(point => point[1]))
    
    for (let i = 0; i < 8; i++) {
      const lat = minLat + Math.random() * (maxLat - minLat)
      const lng = minLng + Math.random() * (maxLng - minLng)
      const aqi = Math.floor(Math.random() * 200) + 50
      airQualityData.push({ lat, lng, aqi })
    }
  } else {
    // Generate air quality data around the current map center (full view)
    for (let i = 0; i < 20; i++) {
      const lat = mapCenter[0] + (Math.random() - 0.5) * 0.05
      const lng = mapCenter[1] + (Math.random() - 0.5) * 0.05
      const aqi = Math.floor(Math.random() * 200) + 50
      airQualityData.push({ lat, lng, aqi })
    }
  }

  return (
    <>
      {airQualityData.map((point, index) => (
        <Circle
          key={index}
          center={[point.lat, point.lng]}
          radius={500}
          pathOptions={{
            color: point.aqi > 150 ? '#ff4444' : point.aqi > 100 ? '#ffaa00' : '#44ff44',
            fillColor: point.aqi > 150 ? '#ff4444' : point.aqi > 100 ? '#ffaa00' : '#44ff44',
            fillOpacity: 0.3,
            weight: 2
          }}
        >
          <Popup>
            <div className="p-2">
              <h3 className="font-semibold text-gray-800">Air Quality Station</h3>
              <p className="text-sm">AQI: {point.aqi}</p>
              <p className="text-sm text-gray-600">
                {point.aqi > 150 ? 'Unhealthy' : point.aqi > 100 ? 'Moderate' : 'Good'}
              </p>
            </div>
          </Popup>
        </Circle>
      ))}
    </>
  )
})

// Flood Risk Layer Component
const FloodRiskLayer = memo(function FloodRiskLayer() {
  const layers = useStore((state) => state.layers)
  const mapCenter = useStore((state) => state.mapCenter)
  const selectedArea = useStore((state) => state.selectedArea)

  if (!layers.flood) return null

  // Generate mock flood risk areas
  const floodAreas = []
  
  if (selectedArea && selectedArea.bounds) {
    // Generate flood risk areas only within the selected area
    const bounds = selectedArea.bounds
    const minLat = Math.min(...bounds.map(point => point[0]))
    const maxLat = Math.max(...bounds.map(point => point[0]))
    const minLng = Math.min(...bounds.map(point => point[1]))
    const maxLng = Math.max(...bounds.map(point => point[1]))
    
    for (let i = 0; i < 3; i++) {
      const centerLat = minLat + Math.random() * (maxLat - minLat)
      const centerLng = minLng + Math.random() * (maxLng - minLng)
      const risk = Math.random()
      
      // Create polygon around center point
      const polygon = [
        [centerLat - 0.005, centerLng - 0.005],
        [centerLat + 0.005, centerLng - 0.005],
        [centerLat + 0.005, centerLng + 0.005],
        [centerLat - 0.005, centerLng + 0.005],
      ]
      
      floodAreas.push({ polygon, risk })
    }
  } else {
    // Generate flood risk areas around the current map center (full view)
    for (let i = 0; i < 5; i++) {
      const centerLat = mapCenter[0] + (Math.random() - 0.5) * 0.02
      const centerLng = mapCenter[1] + (Math.random() - 0.5) * 0.02
      const risk = Math.random()
      
      // Create polygon around center point
      const polygon = [
        [centerLat - 0.005, centerLng - 0.005],
        [centerLat + 0.005, centerLng - 0.005],
        [centerLat + 0.005, centerLng + 0.005],
        [centerLat - 0.005, centerLng + 0.005],
      ]
      
      floodAreas.push({ polygon, risk })
    }
  }

  return (
    <>
      {floodAreas.map((area, index) => (
        <Polygon
          key={index}
          positions={area.polygon}
          pathOptions={{
            color: area.risk > 0.7 ? '#ff0000' : area.risk > 0.4 ? '#ffaa00' : '#0000ff',
            fillColor: area.risk > 0.7 ? '#ff0000' : area.risk > 0.4 ? '#ffaa00' : '#0000ff',
            fillOpacity: 0.4,
            weight: 2
          }}
        >
          <Popup>
            <div className="p-2">
              <h3 className="font-semibold text-gray-800">Flood Risk Area</h3>
              <p className="text-sm">
                Risk Level: {area.risk > 0.7 ? 'High' : area.risk > 0.4 ? 'Medium' : 'Low'}
              </p>
              <p className="text-sm text-gray-600">
                Probability: {Math.round(area.risk * 100)}%
              </p>
            </div>
          </Popup>
        </Polygon>
      ))}
    </>
  )
})

// Green Space Layer Component
const GreenSpaceLayer = memo(function GreenSpaceLayer() {
  const layers = useStore((state) => state.layers)
  const mapCenter = useStore((state) => state.mapCenter)
  const selectedArea = useStore((state) => state.selectedArea)

  if (!layers.green) return null

  // Generate mock green space data
  const greenSpaces = []
  
  if (selectedArea && selectedArea.bounds) {
    // Generate green space data only within the selected area
    const bounds = selectedArea.bounds
    const minLat = Math.min(...bounds.map(point => point[0]))
    const maxLat = Math.max(...bounds.map(point => point[0]))
    const minLng = Math.min(...bounds.map(point => point[1]))
    const maxLng = Math.max(...bounds.map(point => point[1]))
    
    for (let i = 0; i < 8; i++) {
      const lat = minLat + Math.random() * (maxLat - minLat)
      const lng = minLng + Math.random() * (maxLng - minLng)
      const coverage = Math.random()
      greenSpaces.push({ lat, lng, coverage })
    }
  } else {
    // Generate green space data around the current map center (full view)
    for (let i = 0; i < 15; i++) {
      const lat = mapCenter[0] + (Math.random() - 0.5) * 0.08
      const lng = mapCenter[1] + (Math.random() - 0.5) * 0.08
      const coverage = Math.random()
      greenSpaces.push({ lat, lng, coverage })
    }
  }

  return (
    <>
      {greenSpaces.map((space, index) => (
        <Circle
          key={index}
          center={[space.lat, space.lng]}
          radius={300}
          pathOptions={{
            color: '#00aa00',
            fillColor: '#00aa00',
            fillOpacity: space.coverage * 0.6,
            weight: 2
          }}
        >
          <Popup>
            <div className="p-2">
              <h3 className="font-semibold text-gray-800">Green Space</h3>
              <p className="text-sm">Coverage: {Math.round(space.coverage * 100)}%</p>
              <p className="text-sm text-gray-600">
                {space.coverage > 0.7 ? 'High' : space.coverage > 0.4 ? 'Medium' : 'Low'} Density
              </p>
            </div>
          </Popup>
        </Circle>
      ))}
    </>
  )
})

// Contour Lines Layer Component
const ContourLinesLayer = memo(function ContourLinesLayer() {
  const showContours = useStore((state) => state.showContours)
  const mapCenter = useStore((state) => state.mapCenter)
  const selectedArea = useStore((state) => state.selectedArea)

  if (!showContours) return null

  // Generate mock contour lines
  const contourLines = []
  const elevations = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
  
  if (selectedArea && selectedArea.bounds) {
    // Generate contour lines only within the selected area
    const bounds = selectedArea.bounds
    const centerLat = bounds.reduce((sum, point) => sum + point[0], 0) / bounds.length
    const centerLng = bounds.reduce((sum, point) => sum + point[1], 0) / bounds.length
    const maxRadius = Math.min(
      Math.max(...bounds.map(point => Math.abs(point[0] - centerLat))),
      Math.max(...bounds.map(point => Math.abs(point[1] - centerLng)))
    ) * 0.8
    
    elevations.forEach((elevation, index) => {
      const radius = (index / elevations.length) * maxRadius
      const numPoints = 20
      
      const contour = []
      for (let i = 0; i < numPoints; i++) {
        const angle = (i / numPoints) * 2 * Math.PI
        const lat = centerLat + radius * Math.cos(angle)
        const lng = centerLng + radius * Math.sin(angle)
        contour.push([lat, lng])
      }
      
      contourLines.push({
        points: contour,
        elevation: elevation
      })
    })
  } else {
    // Generate contour lines around the current map center (full view)
    elevations.forEach((elevation, index) => {
      const radius = 0.02 + (index * 0.005) // Increasing radius for higher elevations
      const numPoints = 20
      
      const contour = []
      for (let i = 0; i < numPoints; i++) {
        const angle = (i / numPoints) * 2 * Math.PI
        const lat = mapCenter[0] + radius * Math.cos(angle)
        const lng = mapCenter[1] + radius * Math.sin(angle)
        contour.push([lat, lng])
      }
      
      contourLines.push({
        points: contour,
        elevation: elevation
      })
    })
  }

  return (
    <>
      {contourLines.map((line, index) => (
        <Polyline
          key={index}
          positions={line.points}
          pathOptions={{
            color: line.elevation > 500 ? '#8B4513' : line.elevation > 300 ? '#654321' : '#228B22',
            weight: 1,
            opacity: 0.7
          }}
        >
          <Popup>
            <div className="p-2">
              <h3 className="font-semibold text-gray-800">Contour Line</h3>
              <p className="text-sm">Elevation: {line.elevation}m</p>
            </div>
          </Popup>
        </Polyline>
      ))}
    </>
  )
})

// Elevation Markers Layer Component
const ElevationMarkersLayer = memo(function ElevationMarkersLayer() {
  const elevationProfile = useStore((state) => state.elevationProfile)

  if (!elevationProfile) return null

  return (
    <>
      {elevationProfile.map((point, index) => (
        <Circle
          key={index}
          center={[point.lat, point.lng]}
          radius={100}
          pathOptions={{
            color: point.elevation > 1000 ? '#8B0000' : point.elevation > 500 ? '#FF4500' : '#32CD32',
            fillColor: point.elevation > 1000 ? '#8B0000' : point.elevation > 500 ? '#FF4500' : '#32CD32',
            fillOpacity: 0.3,
            weight: 2
          }}
        >
          <Popup>
            <div className="p-2">
              <h3 className="font-semibold text-gray-800">Elevation Point</h3>
              <p className="text-sm">Elevation: {point.elevation.toFixed(0)}m</p>
              <p className="text-sm text-gray-600">
                Distance: {point.distance.toFixed(2)}°
              </p>
            </div>
          </Popup>
        </Circle>
      ))}
    </>
  )
})

// Selected Area Layer Component - Shows the permanent selected area
const SelectedAreaLayer = memo(function SelectedAreaLayer() {
  const selectedArea = useStore((state) => state.selectedArea)

  if (!selectedArea || !selectedArea.bounds) return null

  // Create rectangle from bounds
  const bounds = selectedArea.bounds
  const rectangleBounds = [
    [bounds[0][0], bounds[0][1]],
    [bounds[0][0], bounds[1][1]],
    [bounds[1][0], bounds[1][1]],
    [bounds[1][0], bounds[0][1]]
  ]

  return (
    <Polygon
      positions={rectangleBounds}
      pathOptions={{
        color: '#00aaff',
        fillColor: '#00aaff',
        fillOpacity: 0.1,
        weight: 3,
        dashArray: '8, 4'
      }}
    >
      <Popup>
        <div className="p-2">
          <h3 className="font-semibold text-gray-800">Selected Area</h3>
          <p className="text-sm">Area: {selectedArea.area} km²</p>
          <p className="text-sm text-gray-600">
            Click "Focus on Area" to zoom to this region
          </p>
        </div>
      </Popup>
    </Polygon>
  )
})

// Map Interaction Handler
const MapInteractionHandler = memo(function MapInteractionHandler() {
  const { setSelectionMode, selectionMode, setSelectedArea, setSelectedAreaData, selectionBox, setSelectionBox } = useStore()
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState(null)

  useMapEvents({
    mousedown(e) {
      if (selectionMode) {
        const { lat, lng } = e.latlng
        setDragStart([lat, lng])
        setIsDragging(true)
        setSelectionBox(null) // Clear temporary selection box only
      }
    },
    mousemove(e) {
      if (selectionMode && isDragging && dragStart) {
        const { lat, lng } = e.latlng
        const bounds = [
          [Math.min(dragStart[0], lat), Math.min(dragStart[1], lng)],
          [Math.max(dragStart[0], lat), Math.max(dragStart[1], lng)]
        ]
        setSelectionBox(bounds)
      }
    },
    mouseup(e) {
      if (selectionMode && isDragging && dragStart) {
        const { lat, lng } = e.latlng
        const bounds = [
          [Math.min(dragStart[0], lat), Math.min(dragStart[1], lng)],
          [Math.max(dragStart[0], lat), Math.max(dragStart[1], lng)]
        ]
        
        // Calculate area (simplified)
        const latDiff = bounds[1][0] - bounds[0][0]
        const lngDiff = bounds[1][1] - bounds[0][1]
        const area = Math.abs(latDiff * lngDiff) * 111 * 111 // Rough km² calculation
        
        const selectedArea = {
          area: area.toFixed(2),
          bounds: bounds
        }
        
        // Generate mock analysis data
        const analysisData = {
          population: Math.floor(Math.random() * 50000) + 5000,
          heatIndex: Math.floor(Math.random() * 15) + 25,
          airQuality: Math.floor(Math.random() * 150) + 50,
          greenCoverage: Math.floor(Math.random() * 60) + 20,
          waterStress: Math.floor(Math.random() * 40) + 10,
          floodRisk: Math.random() > 0.5 ? 'Low' : 'Medium',
          buildings: Math.floor(Math.random() * 5000) + 500
        }
        
        setSelectedArea(selectedArea)
        setSelectedAreaData(analysisData)
        setSelectionMode(false)
        setIsDragging(false)
        setDragStart(null)
        setSelectionBox(null)
      }
    }
  })

  // Clear selection when exiting selection mode
  useEffect(() => {
    if (!selectionMode) {
      setIsDragging(false)
      setDragStart(null)
      setSelectionBox(null)
    }
  }, [selectionMode, setSelectionBox])

  // Render temporary selection rectangle if in selection mode
  if (selectionMode && selectionBox) {
    const rectangleBounds = [
      [selectionBox[0][0], selectionBox[0][1]],
      [selectionBox[0][0], selectionBox[1][1]],
      [selectionBox[1][0], selectionBox[1][1]],
      [selectionBox[1][0], selectionBox[0][1]]
    ]
    
    return (
      <Polygon
        positions={rectangleBounds}
        pathOptions={{
          color: '#ffff00',
          fillColor: '#ffff00',
          fillOpacity: 0.3,
          weight: 3,
          dashArray: '10, 5'
        }}
      />
    )
  }

  return null
})

// Selection Mode Indicator
const SelectionModeIndicator = memo(function SelectionModeIndicator() {
  const selectionMode = useStore((state) => state.selectionMode)

  if (!selectionMode) return null

  return (
    <div className="absolute top-20 right-6 z-[1000] bg-blue-600/95 backdrop-blur-md rounded-lg p-4 border-2 border-blue-400/70 shadow-lg">
      <div className="flex items-center gap-3 text-blue-100">
        <div className="w-6 h-6 flex items-center justify-center">
          <div className="w-4 h-4 border-2 border-blue-200 rounded-sm"></div>
        </div>
        <div>
          <div className="text-sm font-bold">SELECTION MODE</div>
          <div className="text-xs text-blue-200 font-normal">
            Cursor: Crosshair (+) - Click & drag to select area
          </div>
          <div className="text-xs text-blue-300 font-normal mt-1">
            Map dragging disabled
          </div>
        </div>
      </div>
    </div>
  )
})

// Base layer URLs
const baseLayers = {
  satellite: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  topographic: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
  terrain: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
  streets: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
}

// Memoize the entire map container
export default memo(function MapContainer() {
  // Selective subscriptions
  const mapCenter = useStore((state) => state.mapCenter)
  const mapZoom = useStore((state) => state.mapZoom)
  const baseLayer = useStore((state) => state.baseLayer)
  const selectionMode = useStore((state) => state.selectionMode)

  return (
    <section 
      className={`relative bg-white/10 rounded-2xl overflow-hidden border border-white/20 ${
        selectionMode ? 'selection-mode' : ''
      }`}
      style={{
        cursor: selectionMode ? 'crosshair' : 'default'
      }}
    >
      <LeafletMap
        center={mapCenter}
        zoom={mapZoom}
        style={{ 
          height: '100%', 
          width: '100%',
          cursor: selectionMode ? 'crosshair !important' : 'default'
        }}
        zoomControl={!selectionMode}
        zoomControlProps={{
          position: 'topright'
        }}
        attributionControl={false}
        dragging={!selectionMode}
        doubleClickZoom={!selectionMode}
        scrollWheelZoom={!selectionMode}
        touchZoom={!selectionMode}
        boxZoom={!selectionMode}
        keyboard={!selectionMode}
      >
        <TileLayer
          url={baseLayers[baseLayer] || baseLayers.satellite}
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {/* Map Controllers */}
        <MapController />
        <MapInteractionHandler />
        
        {/* Data Layers */}
        <HeatMapLayer />
        <AirQualityLayer />
        <FloodRiskLayer />
        <GreenSpaceLayer />
        <ContourLinesLayer />
        <ElevationMarkersLayer />
        <SelectedAreaLayer />
      </LeafletMap>
      
      <StatusPanel />
      <SelectionModeIndicator />
      <MapLegend />
    </section>
  )
})


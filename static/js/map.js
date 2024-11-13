document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map', {
        center: [40, 100],
        zoom: 3,
        minZoom: 2,
        maxBounds: [
            [-90, -180],
            [90, 180]
        ],
        maxBoundsViscosity: 1.0,
        worldCopyJump: true
    });
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    const locationMap = new Map();
    
    const colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD',
        '#D4A5A5', '#9B59B6', '#3498DB', '#FF8C94', '#7FB069',
        '#E67E22', '#CD84F1'
    ];

    function getRandomColor() {
        return colors[Math.floor(Math.random() * colors.length)];
    }

    function getAdjustedCoordinates(lat, lng, locationKey) {
        if (locationMap.has(locationKey)) {
            const count = locationMap.get(locationKey);
            locationMap.set(locationKey, count + 1);
            
            const angle = (count * 45) % 360;
            const radius = 0.02;
            const rad = angle * (Math.PI / 180);
            
            return {
                lat: lat + radius * Math.sin(rad),
                lng: lng + radius * Math.cos(rad)
            };
        } else {
            locationMap.set(locationKey, 1);
            return { lat, lng };
        }
    }

    users.forEach(user => {
        if (user.coordinates) {
            const locationKey = `${user.city}-${user.country}`;
            const adjustedCoords = getAdjustedCoordinates(
                user.coordinates.lat,
                user.coordinates.lng,
                locationKey
            );

            const markerColor = getRandomColor();
            
            const customIcon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="
                    background-color: ${markerColor}; 
                    width: 50px; 
                    height: 50px; 
                    border-radius: 50%; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    color: white; 
                    font-weight: bold; 
                    font-size: 20px;
                    border: 3px solid white; 
                    box-shadow: 0 3px 8px rgba(0,0,0,0.3);">
                        ${user.name.charAt(0).toUpperCase()}
                    </div>`,
                iconSize: [50, 50],
                iconAnchor: [25, 25],
                popupAnchor: [0, -30]
            });

            const marker = L.marker([adjustedCoords.lat, adjustedCoords.lng], {
                icon: customIcon
            }).addTo(map);

            const popupContent = `
                <div class="custom-popup" style="color: ${markerColor}">
                    <h2>${user.name}</h2>
                    <div class="story">${user.story}</div>
                    <div class="image-container">
                        <img src="/uploads/${user.photo}" alt="${user.name}'s photo">
                    </div>
                </div>
            `;
            
            const popup = L.popup({
                maxWidth: window.innerWidth <= 768 ? 280 : 500,
                className: 'custom-popup-wrapper',
                closeButton: true,
                autoPan: true
            }).setContent(popupContent);
            
            marker.bindPopup(popup);

            // 修改 tooltip 的位置到 marker 下方
            marker.bindTooltip(user.name, {
                permanent: false,
                direction: 'bottom',  // 改为 bottom
                className: 'marker-tooltip',
                offset: [0, 30]      // 调整偏移量，正值会向下偏移
            });
        }
    });
});
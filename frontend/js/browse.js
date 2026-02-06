// Browse Cars JavaScript

let allCars = [];
let filteredCars = [];

document.addEventListener('DOMContentLoaded', async () => {
    // Set minimum dates
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('filterPickupDate').min = today;
    document.getElementById('filterReturnDate').min = today;

    // Load locations
    await loadLocations();

    // Load cars
    await loadCars();

    // Check URL parameters
    applyURLParams();

    // Setup event listeners
    setupEventListeners();
});

async function loadLocations() {
    try {
        const locations = await CarRental.apiRequest('/locations');
        const select = document.getElementById('filterLocation');

        locations.forEach(location => {
            const option = document.createElement('option');
            option.value = location.id;
            option.textContent = `${location.name}, ${location.city}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load locations:', error);
    }
}

async function loadCars() {
    try {
        allCars = await CarRental.apiRequest('/cars');
        filteredCars = [...allCars];
        displayCars(filteredCars);
    } catch (error) {
        console.error('Failed to load cars:', error);
        document.getElementById('resultsInfo').textContent = 'Failed to load cars';
    }
}

function displayCars(cars) {
    const grid = document.getElementById('carsGrid');
    const noResults = document.getElementById('noCarsMessage');
    const resultsInfo = document.getElementById('resultsInfo');

    grid.innerHTML = '';

    if (cars.length === 0) {
        noResults.classList.remove('hidden');
        resultsInfo.textContent = 'No cars found';
        return;
    }

    noResults.classList.add('hidden');
    resultsInfo.textContent = `Showing ${cars.length} car${cars.length !== 1 ? 's' : ''}`;

    cars.forEach(car => {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.cursor = 'pointer';
        card.innerHTML = `
            <div class="card-image-container">
                <img src="${car.image_url}" alt="${car.name}" class="card-image" 
                     onerror="this.src='https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800'">
                <div class="card-badge">${car.car_type}</div>
            </div>
            <div class="card-content">
                <h3 class="card-title">${car.name}</h3>
                <p class="card-subtitle">📍 ${car.location_name}, ${car.city}</p>
                <div class="card-features">
                    <span class="feature-tag">👥 ${car.seats} Seats</span>
                    <span class="feature-tag">⚙️ ${car.transmission}</span>
                    <span class="feature-tag">⛽ ${car.fuel_type}</span>
                </div>
                <div class="card-price">
                    <div>
                        <div class="price">$${car.price_per_day}</div>
                        <div class="price-label">per day</div>
                    </div>
                    <button class="btn btn-primary view-details-btn" data-car-id="${car.id}">View Details</button>
                </div>
            </div>
        `;

        card.addEventListener('click', (e) => {
            if (!e.target.classList.contains('view-details-btn')) {
                window.location.href = `/car-details.html?id=${car.id}`;
            }
        });

        const viewBtn = card.querySelector('.view-details-btn');
        viewBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            window.location.href = `/car-details.html?id=${car.id}`;
        });

        grid.appendChild(card);
    });
}

function applyFilters() {
    const locationId = document.getElementById('filterLocation').value;
    const carType = document.getElementById('filterType').value;
    const minPrice = parseFloat(document.getElementById('filterMinPrice').value) || 0;
    const maxPrice = parseFloat(document.getElementById('filterMaxPrice').value) || Infinity;

    filteredCars = allCars.filter(car => {
        if (locationId && car.location_id != locationId) return false;
        if (carType && car.car_type !== carType) return false;
        if (car.price_per_day < minPrice || car.price_per_day > maxPrice) return false;
        return true;
    });

    displayCars(filteredCars);
}

function clearFilters() {
    document.getElementById('filterLocation').value = '';
    document.getElementById('filterType').value = '';
    document.getElementById('filterMinPrice').value = '';
    document.getElementById('filterMaxPrice').value = '';
    document.getElementById('filterPickupDate').value = '';
    document.getElementById('filterReturnDate').value = '';

    filteredCars = [...allCars];
    displayCars(filteredCars);

    // Clear URL parameters
    window.history.replaceState({}, '', '/browse.html');
}

function applyURLParams() {
    const params = new URLSearchParams(window.location.search);

    if (params.has('location')) {
        document.getElementById('filterLocation').value = params.get('location');
    }
    if (params.has('pickup')) {
        document.getElementById('filterPickupDate').value = params.get('pickup');
    }
    if (params.has('return')) {
        document.getElementById('filterReturnDate').value = params.get('return');
    }

    if (params.has('location') || params.has('pickup') || params.has('return')) {
        applyFilters();
    }
}

function setupEventListeners() {
    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    document.getElementById('clearFilters').addEventListener('click', clearFilters);

    // Apply filters on Enter key
    document.querySelectorAll('.filter-sidebar input, .filter-sidebar select').forEach(element => {
        element.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
    });
}

// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', async () => {
    // Check if user is logged in
    if (!CarRental.isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }

    const user = CarRental.getCurrentUser();
    document.getElementById('welcomeMessage').textContent = `Welcome, ${user.full_name}!`;

    await loadBookings();
});

async function loadBookings() {
    try {
        const bookings = await CarRental.apiRequest('/bookings');
        displayBookings(bookings);
    } catch (error) {
        console.error('Failed to load bookings:', error);
        CarRental.showAlert('Failed to load bookings', 'error');
    }
}

function displayBookings(bookings) {
    const container = document.getElementById('bookingsList');
    const noBookings = document.getElementById('noBookings');

    if (bookings.length === 0) {
        container.classList.add('hidden');
        noBookings.classList.remove('hidden');
        return;
    }

    container.classList.remove('hidden');
    noBookings.classList.add('hidden');

    container.innerHTML = bookings.map(booking => `
        <div class="booking-card">
            <div style="display: grid; grid-template-columns: 200px 1fr auto; gap: 1.5rem; align-items: center;">
                <img src="${booking.image_url}" alt="${booking.car_name}" 
                     style="width: 100%; height: 120px; object-fit: cover; border-radius: var(--radius-md);"
                     onerror="this.src='https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=400'">
                
                <div>
                    <h3 style="margin-bottom: 0.5rem;">${booking.car_name}</h3>
                    <p style="color: var(--gray-600); margin-bottom: 0.5rem;">
                        ${booking.brand} ${booking.model}
                    </p>
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
                        <span style="color: var(--gray-700);">
                            📅 ${CarRental.formatDate(booking.pickup_date)} - ${CarRental.formatDate(booking.return_date)}
                        </span>
                        <span style="color: var(--gray-700);">
                            📍 ${booking.pickup_location_name}
                        </span>
                    </div>
                </div>

                <div style="text-align: right;">
                    <div class="booking-status status-${booking.status}" style="margin-bottom: 1rem;">
                        ${booking.status}
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--primary); margin-bottom: 1rem;">
                        ${CarRental.formatCurrency(booking.total_price)}
                    </div>
                    ${booking.status === 'confirmed' ? `
                        <button onclick="cancelBooking(${booking.id})" class="btn btn-outline" style="font-size: 0.875rem;">
                            Cancel Booking
                        </button>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) {
        return;
    }

    try {
        await CarRental.apiRequest(`/bookings/${bookingId}`, {
            method: 'DELETE'
        });

        CarRental.showAlert('Booking cancelled successfully', 'success');
        await loadBookings();
    } catch (error) {
        CarRental.showAlert(error.message, 'error');
    }
}

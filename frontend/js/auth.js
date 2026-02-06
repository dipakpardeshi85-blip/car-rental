// Authentication JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    // Login Form Handler
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await CarRental.apiRequest('/login', {
                    method: 'POST',
                    body: JSON.stringify({ email, password })
                });

                CarRental.setCurrentUser(response.user);
                showAlert('Login successful! Redirecting...', 'success');

                setTimeout(() => {
                    window.location.href = '/dashboard.html';
                }, 1000);
            } catch (error) {
                showAlert(error.message, 'error');
            }
        });
    }

    // Register Form Handler
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const fullName = document.getElementById('fullName').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            // Validation
            if (!CarRental.validateEmail(email)) {
                showAlert('Please enter a valid email address', 'error');
                return;
            }

            if (!CarRental.validatePhone(phone)) {
                showAlert('Please enter a valid phone number', 'error');
                return;
            }

            if (password.length < 6) {
                showAlert('Password must be at least 6 characters long', 'error');
                return;
            }

            if (password !== confirmPassword) {
                showAlert('Passwords do not match', 'error');
                return;
            }

            try {
                const response = await CarRental.apiRequest('/register', {
                    method: 'POST',
                    body: JSON.stringify({
                        full_name: fullName,
                        email,
                        phone,
                        password
                    })
                });

                CarRental.setCurrentUser(response.user);
                showAlert('Registration successful! Redirecting...', 'success');

                setTimeout(() => {
                    window.location.href = '/dashboard.html';
                }, 1000);
            } catch (error) {
                showAlert(error.message, 'error');
            }
        });
    }
});

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    container.innerHTML = '';
    container.appendChild(alert);
}

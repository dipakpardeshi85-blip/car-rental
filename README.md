# DriveNow - Car Rental Website

A full-stack car rental website built with HTML, CSS, JavaScript frontend and Python Flask backend with SQL database.

## Features

### User Features
- 🚗 Browse cars from multiple locations
- 🔍 Filter cars by location, type, and price range
- 📅 Book cars with date selection
- 👤 User authentication (register/login)
- 📊 Personal dashboard to manage bookings
- ❌ Cancel bookings

### Admin Features
- ➕ Add new cars to the fleet
- 📝 Edit existing car details
- 👀 View all bookings across the platform

### Technical Features
- Modern, responsive design with glassmorphism effects
- RESTful API architecture
- Session-based authentication with bcrypt password hashing
- SQLite database with sample data
- Real-time availability checking
- Dynamic price calculation

## Technology Stack

**Frontend:**
- HTML5
- CSS3 (Modern design with gradients, animations, glassmorphism)
- Vanilla JavaScript (ES6+)

**Backend:**
- Python 3.x
- Flask web framework
- Flask-CORS for cross-origin requests
- bcrypt for password hashing

**Database:**
- SQLite (easily upgradeable to PostgreSQL/MySQL)

## Project Structure

```
car-rental-website/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── database.py         # Database operations
│   ├── auth.py             # Authentication routes
│   ├── api.py              # API endpoints
│   ├── schema.sql          # Database schema
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Homepage
│   ├── browse.html         # Car browsing page
│   ├── car-details.html    # Car details page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard.html      # User dashboard
│   ├── admin.html          # Admin panel
│   ├── css/
│   │   └── styles.css      # Main stylesheet
│   └── js/
│       ├── main.js         # Utility functions
│       ├── auth.js         # Authentication logic
│       ├── browse.js       # Browse page logic
│       └── dashboard.js    # Dashboard logic
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Initialize Database

The database will be automatically initialized when you first run the application. It includes:
- 6 locations across major US cities
- 12 sample cars with different types and prices
- 1 admin user account

### Step 3: Start the Server

```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

### Step 4: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Default Credentials

**Admin Account:**
- Email: `admin@carrental.com`
- Password: `admin123`

You can create new user accounts through the registration page.

## Sample Data

The database comes pre-populated with:

**Locations:**
- New York (Downtown Hub)
- Los Angeles (Airport Center)
- Miami (Beach Station)
- Chicago (City Center)
- San Francisco (Tech District)
- Boston (Historic Quarter)

**Cars:** 12 vehicles including:
- Tesla Model 3 Performance
- BMW X5 M Sport
- Mercedes-Benz C-Class
- Porsche 911 Carrera
- Range Rover Sport
- And more...

## API Endpoints

### Authentication
- `POST /api/register` - Create new user account
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user
- `GET /api/user` - Get current user info

### Cars
- `GET /api/locations` - Get all locations
- `GET /api/cars` - Get cars (with optional filters)
- `GET /api/cars/<id>` - Get car details
- `POST /api/cars/check-availability` - Check car availability

### Bookings
- `POST /api/bookings` - Create new booking
- `GET /api/bookings` - Get user's bookings
- `DELETE /api/bookings/<id>` - Cancel booking

### Admin
- `POST /api/admin/cars` - Add new car
- `PUT /api/admin/cars/<id>` - Update car
- `GET /api/admin/bookings` - Get all bookings

## Usage Guide

### For Users

1. **Browse Cars:**
   - Visit the homepage and use the quick search widget
   - Or go to Browse Cars to see all available vehicles
   - Apply filters to narrow down your search

2. **Book a Car:**
   - Click on any car to view details
   - Click "Book This Car"
   - Login or register if not already logged in
   - Select pickup and return dates
   - Confirm booking

3. **Manage Bookings:**
   - Go to Dashboard to view your bookings
   - Cancel bookings if needed

### For Admins

1. **Add New Cars:**
   - Login with admin credentials
   - Go to Admin Panel
   - Fill out the car details form
   - Submit to add the car to the fleet

2. **View All Bookings:**
   - Scroll down in the Admin Panel
   - See all bookings across all users

## Design Features

- **Modern Gradient Backgrounds:** Eye-catching hero sections
- **Glassmorphism:** Translucent cards with backdrop blur
- **Smooth Animations:** Fade-in effects and hover transitions
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Premium Typography:** Google Fonts (Inter & Outfit)
- **Intuitive Navigation:** Clear user flows and CTAs

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- CSRF protection via Flask sessions
- Input validation on both frontend and backend
- SQL injection prevention through parameterized queries

## Future Enhancements

Potential features to add:
- Payment integration (Stripe, PayPal)
- Email notifications for bookings
- User reviews and ratings
- Car availability calendar view
- Multi-language support
- Advanced search with more filters
- Image upload for cars
- Booking modifications
- Loyalty program

## Deployment on Render

This application is configured for easy deployment on [Render](https://render.com).

### Prerequisites

- GitHub account with this repository pushed
- Render account (free tier available)

### Deployment Steps

1. **Push Code to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Create New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `dipakpardeshi85-blip/car-rental`
   - Render will auto-detect the `render.yaml` configuration

3. **Configure Environment Variables** (Optional)
   - Render will auto-generate `SECRET_KEY`
   - All other settings are configured in `render.yaml`

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - Wait for the build to complete (usually 2-5 minutes)

5. **Access Your Application**
   - Once deployed, Render provides a URL like: `https://car-rental-website-xxxx.onrender.com`
   - Visit the URL to access your live application

### Important Notes

> **Database Persistence**: The free tier uses ephemeral storage. The SQLite database will reset on each deployment or when the service restarts. For production use, consider:
> - Upgrading to a paid plan with persistent disk
> - Migrating to PostgreSQL (Render offers free PostgreSQL databases)

> **Cold Starts**: Free tier services spin down after 15 minutes of inactivity. The first request after inactivity may take 30-60 seconds.

### Environment Variables

The following environment variables are automatically configured:

- `SECRET_KEY` - Auto-generated by Render for session security
- `FLASK_ENV` - Set to `production`
- `PORT` - Auto-assigned by Render
- `RENDER_EXTERNAL_URL` - Auto-set by Render for CORS

### Updating Your Deployment

Render automatically redeploys when you push to the `main` branch:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

### Troubleshooting Render Deployment

**Build Fails:**
- Check the build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version compatibility

**Application Won't Start:**
- Check the service logs in Render dashboard
- Verify the start command in `render.yaml`
- Ensure database initializes correctly

**Static Files Not Loading:**
- Render serves both frontend and backend from the same service
- Check that paths in HTML files are relative, not absolute



## Troubleshooting

**Database Issues:**
- Delete `car_rental.db` file and restart the server to reinitialize

**Port Already in Use:**
- Change the port in `app.py`: `app.run(port=5001)`

**CORS Errors:**
- Ensure you're accessing via `http://localhost:5000` not `file://`

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the code comments or review the implementation plan.

---

**Enjoy your car rental experience with DriveNow! 🚗✨**

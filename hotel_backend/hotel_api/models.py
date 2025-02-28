from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model (Guests & Staff)
class User(AbstractUser):  # Extending Django's built-in User model
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
        ('housekeeping', 'Housekeeping'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Staff Model (Only for employees)
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    permissions = models.JSONField(default=dict)  # Store access control
    created_at = models.DateTimeField(auto_now_add=True)

# Rooms Model
class Room(models.Model):
    ROOM_TYPES = [('single', 'Single'), ('double', 'Double'), ('suite', 'Suite')]
    STATUS_CHOICES = [('available', 'Available'), ('booked', 'Booked'), ('occupied', 'Occupied'), ('cleaning', 'Cleaning')]

    room_number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    features = models.JSONField(default=dict)  # Store extra features like Wi-Fi, AC
    created_at = models.DateTimeField(auto_now_add=True)

# Bookings Model
class Booking(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('checked-in', 'Checked-In'), ('checked-out', 'Checked-Out'), ('cancelled', 'Cancelled')]
    PAYMENT_STATUS_CHOICES = [('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')]

    guest = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'guest'})
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

# Payments Model
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [('card', 'Card'), ('cash', 'Cash'), ('upi', 'UPI')]
    PAYMENT_STATUS_CHOICES = [('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)

# Room Assignments Model
class RoomAssignment(models.Model):
    STATUS_CHOICES = [('assigned', 'Assigned'), ('checked-in', 'Checked-In'), ('checked-out', 'Checked-Out')]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')

# Guest Preferences Model
class GuestPreference(models.Model):
    PREFERENCE_TYPES = [('bed_type', 'Bed Type'), ('temperature', 'Temperature'), ('meal', 'Meal')]

    guest = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'guest'})
    preference_type = models.CharField(max_length=20, choices=PREFERENCE_TYPES)
    value = models.CharField(max_length=100)

    



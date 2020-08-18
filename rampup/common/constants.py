MAX_NAME_LENGTH = 100
MAX_PLACE_LENGTH = 30

PLACED = 1
ACCEPTED = 2
REJECTED = 3
DISPATCHED = 4
DELIVERED = 5
CANCELLED = 6

STATUS_CHOICES = [
    (PLACED, 'placed'),
    (ACCEPTED, 'accepted'),
    (REJECTED, 'rejected'),
    (DISPATCHED, 'dispatched'),
    (DELIVERED, 'delivered'),
    (CANCELLED, 'cancelled')
    ]

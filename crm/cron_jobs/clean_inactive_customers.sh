#!/bin/bash

# Activate virtual environment if needed (adjust path as necessary)
# source 
# Calculate date one year ago
ONE_YEAR_AGO=$(date -d "365 days ago" '+%Y-%m-%d')


# Run Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import datetime
from crm.models import Customer, Order
from django.db.models import Max

# Get customers with no orders since one year ago
cutoff_date = datetime.strptime('$ONE_YEAR_AGO', '%Y-%m-%d').date()
customers = Customer.objects.annotate(last_order=Max('order__created_at')).filter(last_order__lt=cutoff_date)
count = customers.count()
customers.delete()
print(count)
" 2>/dev/null | tail -n 1)

# Log the result with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt

# Make the script executable
chmod +x "$0"


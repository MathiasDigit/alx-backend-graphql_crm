#!/bin/bash

# Script to delete inactive customers (no orders in past year)

# Get current timestamp
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Run Django shell command to delete customers and capture count
deleted_count=$(python3 manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True) | Customer.objects.exclude(order__created_at__gte=one_year_ago)
inactive_customers = inactive_customers.distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

# Log the result
echo "$timestamp - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt

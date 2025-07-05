#!/bin/bash
# Backup script for managed DB
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -F c -b -v -f /backup/backup_$(date +%F_%H-%M-%S).dump

#!/bin/bash
# Restore script for managed DB
pg_restore -h $DB_HOST -U $DB_USER -d $DB_NAME -v $1

#!/bin/bash
# Remediate DB stuck in read-only mode
kubectl exec -it "$1" -- psql -c 'ALTER DATABASE $DB_NAME SET default_transaction_read_only = off;'

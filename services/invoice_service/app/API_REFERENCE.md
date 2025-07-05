# Invoice Service API Reference

## Endpoints

### Generate Invoice
- **POST** `/invoices/generate/{tenant_id}`
- Generates a new invoice for the tenant from usage data.

### List Invoices
- **GET** `/invoices/{tenant_id}`
- Lists all invoices for a tenant.

### Download Invoice PDF
- **GET** `/invoices/{invoice_id}/download`
- Returns the PDF for the invoice.

### Mark Invoice as Paid
- **POST** `/invoices/mark_paid/{invoice_id}`
- Updates invoice status to paid.

### Get Stripe Invoice Metadata
- **GET** `/invoices/stripe/{invoice_id}`
- Fetches Stripe invoice metadata if available.

## Models
- Invoice

See `schemas.py` for model details.

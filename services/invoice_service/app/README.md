# Invoice Service

Generates, stores, and serves tenant invoices for ReqArchitect.

## Features
- Monthly invoice generation from usage data
- PDF invoice generation and download
- Stripe integration for payment tracking (optional)
- Secure tenant scoping and admin controls
- Audit logging and observability

## Endpoints
- `POST /invoices/generate/{tenant_id}`: Generate invoice from usage
- `GET /invoices/{tenant_id}`: List tenant invoices
- `GET /invoices/{invoice_id}/download`: Download invoice PDF
- `POST /invoices/mark_paid/{invoice_id}`: Mark invoice as paid
- `GET /invoices/stripe/{invoice_id}`: Fetch Stripe invoice metadata

## Security
- Only Owner/Admin can access invoices
- Tenant context validated on all endpoints
- Sensitive metadata should be encrypted

## Observability
- Audit logs on invoice generation and download
- Metrics: invoice count, payment rate, overdue count

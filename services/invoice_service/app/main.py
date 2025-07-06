from fastapi import FastAPI, HTTPException, Depends, status, Response
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

app = FastAPI()

# Dependency for security (stub)
def get_current_admin_user():
    # TODO: Implement JWT/role validation
    pass

def validate_tenant_context(tenant_id: str):
    # TODO: Implement tenant scoping
    pass

@app.post("/invoices/generate/{tenant_id}", response_model=schemas.Invoice)
def generate_invoice(tenant_id: str, db: Session = Depends(get_db), user=Depends(get_current_admin_user)):
    validate_tenant_context(tenant_id)
    # TODO: Pull usage from billing_service, calculate line items, generate PDF, store invoice
    raise HTTPException(status_code=501, detail="Not implemented")

@app.get("/invoices/{tenant_id}", response_model=List[schemas.Invoice])
def list_invoices(tenant_id: str, db: Session = Depends(get_db), user=Depends(get_current_admin_user)):
    validate_tenant_context(tenant_id)
    invoices = db.query(models.Invoice).filter_by(tenant_id=tenant_id).all()
    return invoices

@app.get("/invoices/{invoice_id}/download")
def download_invoice(invoice_id: str, db: Session = Depends(get_db), user=Depends(get_current_admin_user)):
    invoice = db.query(models.Invoice).filter_by(invoice_id=invoice_id).first()
    if not invoice or not invoice.pdf_url:
        raise HTTPException(status_code=404, detail="Invoice or PDF not found")
    # TODO: Serve PDF file from storage
    raise HTTPException(status_code=501, detail="Not implemented")

@app.post("/invoices/mark_paid/{invoice_id}")
def mark_invoice_paid(invoice_id: str, db: Session = Depends(get_db), user=Depends(get_current_admin_user)):
    invoice = db.query(models.Invoice).filter_by(invoice_id=invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice.status = "paid"
    db.commit()
    # TODO: Emit audit log, sync with Stripe if needed
    return {"status": "paid"}

@app.get("/invoices/stripe/{invoice_id}")
def get_stripe_invoice(invoice_id: str, db: Session = Depends(get_db), user=Depends(get_current_admin_user)):
    invoice = db.query(models.Invoice).filter_by(invoice_id=invoice_id).first()
    if not invoice or not invoice.stripe_invoice_id:
        raise HTTPException(status_code=404, detail="Stripe invoice not found")
    # TODO: Fetch Stripe invoice metadata
    raise HTTPException(status_code=501, detail="Not implemented")

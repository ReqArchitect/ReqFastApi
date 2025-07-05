from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class InvoiceBase(BaseModel):
    tenant_id: str
    billing_period_start: datetime
    billing_period_end: datetime
    line_items: List[Dict]
    total_amount: float
    status: str
    pdf_url: Optional[str] = None
    stripe_invoice_id: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    invoice_id: str
    class Config:
        orm_mode = True

import os
import logging
import time
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from typing import Dict, Any, Optional

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICE_DIR = os.path.join(os.path.dirname(TEMPLATE_DIR), 'invoices')
os.makedirs(INVOICE_DIR, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_invoice_pdf(invoice: Dict[str, Any], tenant_name: str, billing_email: str, logo_url: Optional[str] = None, brand_color: Optional[str] = None) -> str:
    """
    Renders an invoice as a PDF and saves it to disk.
    Args:
        invoice: Invoice data dict (fields: invoice_id, billing_period_start, billing_period_end, line_items, total_amount, status, timestamp, etc.)
        tenant_name: Name of the tenant
        billing_email: Billing email address
        logo_url: Optional logo image URL or path
        brand_color: Optional brand color hex
    Returns:
        file_path: Path to the generated PDF file
    """
    start_time = time.time()
    logger = logging.getLogger("pdf_invoice_renderer")
    try:
        template = env.get_template("invoice_template.html")
        html_content = template.render(
            invoice_id=invoice["invoice_id"],
            tenant_name=tenant_name,
            billing_period_start=invoice["billing_period_start"],
            billing_period_end=invoice["billing_period_end"],
            status=invoice["status"],
            line_items=invoice["line_items"],
            total_amount=invoice["total_amount"],
            timestamp=invoice.get("timestamp"),
            billing_email=billing_email,
            logo_url=logo_url,
            brand_color=brand_color
        )
        pdf_file = os.path.join(INVOICE_DIR, f"invoice_{invoice['invoice_id']}.pdf")
        HTML(string=html_content, base_url=TEMPLATE_DIR).write_pdf(pdf_file)
        elapsed = time.time() - start_time
        logger.info(f"InvoiceRendered: invoice_id={invoice['invoice_id']} file={pdf_file} time={elapsed:.2f}s")
        # TODO: Emit event to event_bus_service
        return pdf_file
    except Exception as e:
        logger.error(f"Invoice rendering failed: {e}")
        raise

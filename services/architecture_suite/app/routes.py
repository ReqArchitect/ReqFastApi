# --- Linking ArchiMate elements to ArchitecturePackage ---
from fastapi import Body
from .models import ArchitectureElementLink
import uuid

@router.post("/{package_id}/link-element", tags=["ElementLink"])
async def link_archimate_element(
    package_id: UUID,
    element_type: str = Body(..., embed=True),
    element_id: UUID = Body(..., embed=True),
    traceability_fk: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    token_data: deps.TokenData = Depends(deps.require_role(["manager"]))
):
    # Validate package exists and tenant scope
    q = await db.execute(
        "SELECT * FROM architecture_package WHERE id = :id AND tenant_id = :tenant_id",
        {"id": str(package_id), "tenant_id": token_data.tenant_id}
    )
    pkg = q.fetchone()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    # Validate traceability FK exists for this package
    valid_fks = ["business_case_id", "initiative_id", "kpi_id", "business_model_id"]
    if traceability_fk not in valid_fks:
        raise HTTPException(status_code=400, detail="Invalid traceability FK")
    # Insert link
    link = ArchitectureElementLink(
        id=uuid.uuid4(),
        package_id=package_id,
        element_type=element_type,
        element_id=element_id,
        traceability_fk=traceability_fk
    )
    db.add(link)
    await db.commit()
    return {"linked": True, "link_id": str(link.id)}

# --- KPI Impact Summary ---
@router.get("/{package_id}/impact-summary", tags=["Impact"])
async def kpi_impact_summary(
    package_id: UUID,
    db: AsyncSession = Depends(get_db),
    token_data: deps.TokenData = Depends(deps.require_role(ROLES))
):
    # Aggregate KPIs from linked elements
    q = await db.execute(
        "SELECT element_id FROM architecture_element_link WHERE package_id = :pid AND traceability_fk = 'kpi_id'",
        {"pid": str(package_id)}
    )
    kpi_ids = [r[0] for r in q.fetchall()]
    # Compute stats (placeholder logic)
    total = len(kpi_ids)
    aligned = total  # Assume all are aligned for demo
    coverage = 1.0 if total else 0.0
    return {
        "package_id": str(package_id),
        "kpi_count": total,
        "aligned": aligned,
        "coverage": coverage,
        "goal_alignment_score": 1.0 if total else 0.0
    }
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from . import schemas, models, services, deps
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/architecture-packages", tags=["ArchitecturePackage"])

# Dependency placeholder for DB session
# Replace with actual DB session dependency in production

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

# Async DB session setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/architecture_suite")
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# RBAC roles
ROLES = ["superuser", "admin", "manager", "user"]

@router.post("/", response_model=schemas.ArchitecturePackageOut, status_code=201)
async def create_architecture_package(
    payload: schemas.ArchitecturePackageCreate,
    token_data: deps.TokenData = Depends(deps.require_role(["manager"])),
    correlation_id: UUID = Query(..., description="Correlation ID for event traceability"),
    db: AsyncSession = Depends(get_db)
):
    # Enforce tenant/user scoping
    if str(payload.tenant_id) != token_data.tenant_id:
        raise HTTPException(status_code=403, detail="Tenant mismatch.")
    if str(payload.user_id) != token_data.user_id:
        raise HTTPException(status_code=403, detail="User mismatch.")
    # Validate FKs
    fk_checks = [
        ("business_case", payload.business_case_id, "business_case_id"),
        ("initiative", payload.initiative_id, "initiative_id"),
        ("kpi_service", payload.kpi_id, "kpi_id"),
        ("business_model_canvas", payload.business_model_id, "business_model_id")
    ]
    for model, fk, label in fk_checks:
        res = await db.execute(
            f"SELECT id FROM {model} WHERE id = :id AND tenant_id = :tenant_id",
            {"id": str(fk), "tenant_id": str(payload.tenant_id)}
        )
        if not res.scalar():
            raise HTTPException(status_code=400, detail=f"Invalid {label}")
    # Create ArchitecturePackage
    from .models import ArchitecturePackage
    from datetime import datetime
    import uuid
    entity = ArchitecturePackage(
        id=uuid.uuid4(),
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        business_case_id=payload.business_case_id,
        initiative_id=payload.initiative_id,
        kpi_id=payload.kpi_id,
        business_model_id=payload.business_model_id,
        name=payload.name,
        description=payload.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    await services.emit_event(
        event_type="architecture_package_created",
        source_service="architecture_suite",
        entity_id=entity.id,
        tenant_id=entity.tenant_id,
        correlation_id=correlation_id
    )
    return entity

@router.get("/", response_model=List[schemas.ArchitecturePackageOut])
async def list_architecture_packages(
    skip: int = 0,
    limit: int = 10,
    tenant_id: UUID = Query(...),
    user_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
    token_data: deps.TokenData = Depends(deps.require_role(ROLES))
):
    # Only allow users to see their own tenant's data
    if token_data.role == "user" and token_data.tenant_id != str(tenant_id):
        raise HTTPException(status_code=403, detail="Tenant mismatch.")
    from .models import ArchitecturePackage
    q = await db.execute(
        f"SELECT * FROM architecture_package WHERE tenant_id = :tenant_id"
        + (" AND user_id = :user_id" if user_id else ""),
        {"tenant_id": str(tenant_id), "user_id": str(user_id) if user_id else None}
    )
    results = q.fetchall()
    return [dict(r) for r in results]

@router.get("/{package_id}", response_model=schemas.ArchitecturePackageOut)
async def get_architecture_package(
    package_id: UUID,
    tenant_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    token_data: deps.TokenData = Depends(deps.require_role(ROLES))
):
    from .models import ArchitecturePackage
    q = await db.execute(
        f"SELECT * FROM architecture_package WHERE id = :id AND tenant_id = :tenant_id",
        {"id": str(package_id), "tenant_id": str(tenant_id)}
    )
    result = q.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    # Only allow users to see their own tenant's data
    if token_data.role == "user" and token_data.tenant_id != str(tenant_id):
        raise HTTPException(status_code=403, detail="Tenant mismatch.")
    return dict(result)

@router.put("/{package_id}", response_model=schemas.ArchitecturePackageOut)
async def update_architecture_package(
    package_id: UUID,
    payload: schemas.ArchitecturePackageUpdate,
    correlation_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    token_data: deps.TokenData = Depends(deps.require_role(["manager"]))
):
    from .models import ArchitecturePackage
    q = await db.execute(
        f"SELECT * FROM architecture_package WHERE id = :id AND tenant_id = :tenant_id",
        {"id": str(package_id), "tenant_id": token_data.tenant_id}
    )
    entity = q.fetchone()
    if not entity:
        raise HTTPException(status_code=404, detail="Not found")
    # Validate FKs if present
    fk_checks = [
        ("business_case", payload.business_case_id, "business_case_id"),
        ("initiative", payload.initiative_id, "initiative_id"),
        ("kpi_service", payload.kpi_id, "kpi_id"),
        ("business_model_canvas", payload.business_model_id, "business_model_id")
    ]
    for model, fk, label in fk_checks:
        if fk:
            res = await db.execute(
                f"SELECT id FROM {model} WHERE id = :id AND tenant_id = :tenant_id",
                {"id": str(fk), "tenant_id": token_data.tenant_id}
            )
            if not res.scalar():
                raise HTTPException(status_code=400, detail=f"Invalid {label}")
    # Update fields
    update_fields = {k: v for k, v in payload.dict(exclude_unset=True).items()}
    set_clause = ", ".join([f"{k} = :{k}" for k in update_fields])
    update_fields["id"] = str(package_id)
    await db.execute(
        f"UPDATE architecture_package SET {set_clause}, updated_at = now() WHERE id = :id",
        update_fields
    )
    await db.commit()
    await services.emit_event(
        event_type="architecture_package_updated",
        source_service="architecture_suite",
        entity_id=package_id,
        tenant_id=token_data.tenant_id,
        correlation_id=correlation_id
    )
    # Return updated entity
    q = await db.execute(
        f"SELECT * FROM architecture_package WHERE id = :id",
        {"id": str(package_id)}
    )
    return dict(q.fetchone())

@router.delete("/{package_id}", status_code=204)
async def delete_architecture_package(
    package_id: UUID,
    correlation_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    token_data: deps.TokenData = Depends(deps.require_role(["manager"]))
):
    from .models import ArchitecturePackage
    q = await db.execute(
        f"SELECT * FROM architecture_package WHERE id = :id AND tenant_id = :tenant_id",
        {"id": str(package_id), "tenant_id": token_data.tenant_id}
    )
    entity = q.fetchone()
    if not entity:
        raise HTTPException(status_code=404, detail="Not found")
    await db.execute(
        f"DELETE FROM architecture_package WHERE id = :id",
        {"id": str(package_id)}
    )
    await db.commit()
    await services.emit_event(
        event_type="architecture_package_deleted",
        source_service="architecture_suite",
        entity_id=package_id,
        tenant_id=token_data.tenant_id,
        correlation_id=correlation_id
    )
    return JSONResponse(status_code=204)

# Traceability audit endpoint
@router.get("/traceability-check/{package_id}", tags=["Traceability"])
async def traceability_check(
    package_id: UUID,
    db: AsyncSession = Depends(get_db),
    token_data: deps.TokenData = Depends(deps.require_role(ROLES))
):
    # Confirm all FKs resolve
    q = await db.execute(
        f"SELECT * FROM architecture_package WHERE id = :id",
        {"id": str(package_id)}
    )
    entity = q.fetchone()
    if not entity:
        raise HTTPException(status_code=404, detail="Not found")
    missing = []
    fk_checks = [
        ("business_case", entity.business_case_id, "business_case_id"),
        ("initiative", entity.initiative_id, "initiative_id"),
        ("kpi_service", entity.kpi_id, "kpi_id"),
        ("business_model_canvas", entity.business_model_id, "business_model_id")
    ]
    for model, fk, label in fk_checks:
        res = await db.execute(
            f"SELECT id FROM {model} WHERE id = :id AND tenant_id = :tenant_id",
            {"id": str(fk), "tenant_id": entity.tenant_id}
        )
        if not res.scalar():
            missing.append(label)
    return {"package_id": str(package_id), "missing_links": missing}

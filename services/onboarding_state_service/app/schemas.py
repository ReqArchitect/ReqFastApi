from pydantic import BaseModel

class OnboardingStatus(BaseModel):
    tenant_id: str
    user_id: str
    configure_capabilities: bool = False
    create_initiative: bool = False
    invite_teammates: bool = False
    explore_traceability: bool = False
    completed: bool = False

    class Config:
        orm_mode = True

class OnboardingStatusUpdate(BaseModel):
    configure_capabilities: bool | None = None
    create_initiative: bool | None = None
    invite_teammates: bool | None = None
    explore_traceability: bool | None = None

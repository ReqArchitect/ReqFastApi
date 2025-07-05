from sqlalchemy import Column, String, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OnboardingStatus(Base):
    __tablename__ = "onboarding_status"
    tenant_id = Column(String, primary_key=True)
    user_id = Column(String, primary_key=True)
    configure_capabilities = Column(Boolean, default=False)
    create_initiative = Column(Boolean, default=False)
    invite_teammates = Column(Boolean, default=False)
    explore_traceability = Column(Boolean, default=False)

    @property
    def completed(self):
        return all([
            self.configure_capabilities,
            self.create_initiative,
            self.invite_teammates,
            self.explore_traceability
        ])

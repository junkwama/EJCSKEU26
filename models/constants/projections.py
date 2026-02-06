from pydantic import BaseModel
from datetime import datetime

# ============================================================================
# DOCUMENT TYPE PROJECTIONS
# ============================================================================

class DocumentTypeProjFlat(BaseModel):
    """Projection plate de DocumentType - sans relations"""
    id: int
    nom: str

# ============================================================================
# GRADE PROJECTIONS
# ============================================================================

class GradeProjFlat(BaseModel):
    """Projection plate de Grade - sans relations"""
    id: int
    nom: str
    est_supprimee: bool
    date_suppression: datetime | None

# ============================================================================
# FIDELE TYPE PROJECTIONS
# ============================================================================

class FideleTypeProjFlat(BaseModel):
    """Projection plate de FideleType - sans relations"""
    id: int
    nom: str
    est_supprimee: bool
    date_suppression: datetime | None

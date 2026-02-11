from pydantic import BaseModel
from datetime import datetime

# ============================================================================
# DOCUMENT TYPE PROJECTIONS
# ============================================================================

class DocumentTypeProjFlat(BaseModel):
    """Projection plate de DocumentType - sans relations"""
    id: int
    nom: str

    class Config:
        from_attributes = True

# ============================================================================
# GRADE PROJECTIONS
# ============================================================================

class GradeProjFlat(BaseModel):
    """Projection plate de Grade - sans relations"""
    id: int
    nom: str
    est_supprimee: bool
    date_suppression: datetime | None

    class Config:
        from_attributes = True

# ============================================================================
# FIDELE TYPE PROJECTIONS
# ============================================================================

class FideleTypeProjFlat(BaseModel):
    """Projection plate de FideleType - sans relations"""
    id: int
    nom: str
    est_supprimee: bool
    date_suppression: datetime | None

    class Config:
        from_attributes = True

# ============================================================================
# STRUCTURE TYPE PROJECTIONS
# ============================================================================

class StructureTypeProjFlat(BaseModel):
    """Projection plate de StructureType - sans relations"""
    id: int
    nom: str
    est_supprimee: bool
    date_suppression: datetime | None

    class Config:
        from_attributes = True

# ============================================================================
# STRUCTURE PROJECTIONS
# ============================================================================

class StructureProjFlat(BaseModel):
    """Projection plate de Structure - sans relations"""
    id: int
    nom: str
    code: str | None
    description: str | None
    id_structure_type: int
    est_supprimee: bool
    date_suppression: datetime | None

    class Config:
        from_attributes = True

class StructureProjShallow(StructureProjFlat):
    """Projection shallow de Structure - avec relations"""
    structure_type: StructureTypeProjFlat

    class Config:
        from_attributes = True


# ============================================================================
# FONCTION LIST PROJECTIONS
# ============================================================================

class FonctionProjFlat(BaseModel):
    """Projection plate de Fonction - sans relations"""
    id: int
    nom: str
    description: str | None
    ordre: int | None
    id_document_type: int | None
    est_supprimee: bool
    date_suppression: datetime | None

    class Config:
        from_attributes = True

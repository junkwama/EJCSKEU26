from enum import Enum

# ============================================================================
# DOCUMENT TYPE ENUMS
# ============================================================================

class DocumentTypeEnum(int, Enum):
    """Enum pour les types de documents"""
    FIDELE = 1
    PAROISSE = 2
    VILLE = 3
    PROVINCE = 4
    NATION = 5
    CONTINENT = 6
    GENERALE = 7


# ============================================================================
# GRADE ENUMS
# ============================================================================

class GradeEnum(int, Enum):
    """Enum pour les grades ecclésiastiques"""
    MONDIMI = 1
    NKENGI = 2
    LONGI = 3
    SIELO = 4
    PASTEUR = 5


# ============================================================================
# FIDELE TYPE ENUMS
# ============================================================================

class FideleTypeEnum(int, Enum):
    """Enum pour les types de fidèles"""
    PRATIQUANT = 1
    SYMPATHISANT = 2


# ============================================================================
# STRUCTURE TYPE ENUMS
# ============================================================================

class StructureTypeEnum(int, Enum):
    """Enum pour les types de structures"""
    MOUVEMENT = 1
    ASSOCIATION = 2
    SERVICE = 3

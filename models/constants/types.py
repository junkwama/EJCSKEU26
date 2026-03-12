from enum import Enum

# ============================================================================
# DOCUMENT TYPE ENUMS
# ============================================================================

class DocumentTypeEnum(int, Enum):
    """Enum pour les types de documents"""
    FIDELE = 1
    STRUCTURE = 2 # Bureau ecclésiastique, Mouvement, Association, Service
    PAROISSE = 3
    VILLE = 4
    PROVINCE = 5
    NATION = 6
    CONTINENT = 7
    GENERALE = 8


# ============================================================================
# GRADE ENUMS
# ============================================================================

class GradeEnum(int, Enum):
    """Enum pour les grades ecclésiastiques"""
    SANS_GRADE = 1
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
    BUREAU_ECCLESIASTIQUE = 1
    MOUVEMENT = 2
    ASSOCIATION = 3
    SERVICE = 4
    
# ============================================================================
# FONCTION ENUMS
# ============================================================================
class FonctionEnum(int, Enum):
    """Enum pour les fonctions dans une direction"""
    RESPONSABLE_PRESIDENT = 1
    VICE_RESPONSABLE_PRESIDENT_NO1 = 2
    VICE_RESPONSABLE_PRESIDENT_NO2 = 3
    EVANGELISTE = 4
    SECRETAIRE = 5
    SECRETAIRE_ADJOINT = 6
    TRESORIER = 7
    CONSEILLER = 8
    CHEF_DE_CELLULE = 9
    DIRIGEANT_TECHNIQUE = 10
    CHEF_DE_PARTITION = 11
    CHEF_DE_PARTITION_ADJOINT = 12
    
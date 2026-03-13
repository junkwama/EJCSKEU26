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
# STRUCTURE AND STRUCTURE TYPE ENUMS
# ============================================================================

class StructureTypeEnum(int, Enum):
    """Enum pour les types de structures"""
    BUREAU_ECCLESIASTIQUE = 1
    MOUVEMENT = 2
    ASSOCIATION = 3
    SERVICE = 4

class StructureEnum(int, Enum):
    """Enum pour les structures (ex: bureau ecclésiastique)"""
    BUREAU_ECCLESIASTIQUE = 1
    FLUKI = 2
    GTKI = 3
    DIRIGEANTS = 5
    CHOREKI = 6
    GGKI = 7
    AFKI = 8
    UJKI = 9

# ============================================================================
# DOCUMENT STATUT ENUMS
# ============================================================================

class DocumentStatutEnum(int, Enum):
    """Enum pour les statut des entité (docuement)"""
    ATTENTE = 1
    VALIDE = 2
    COMPLETE = 3

# ============================================================================
# RECENSEMENT ETAPE ENUM
# ============================================================================
class RecensementEtapeEnum(int, Enum):
    """Enum pour les étapes du recensement d'un fidèle"""
    INFORMATIONS_DE_BASE = 1
    FAMILLE = 2
    OCCUPATION = 3
    CONTACT = 4
    ADRESSE = 5
    ORIGINES = 6
    BAPTEME = 7
    PAROISSES = 8
    STRUCTURES = 9
    PHOTO_DE_PROFIL = 10


# ============================================================================
# FONCTION ENUM
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
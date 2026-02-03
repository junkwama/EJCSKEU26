-- ============================================================================
-- BASE DE DONNEES: EJCSK - Recencement des Fidèles de l'Église Kimbaguiste
-- ============================================================================

DROP DATABASE IF EXISTS ejcsk;
CREATE DATABASE ejcsk CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ejcsk;

-- ============================================================================
-- TABLE: continent
-- ============================================================================
CREATE TABLE continent (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: nation
-- ============================================================================
CREATE TABLE nation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    id_continent INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_continent) REFERENCES continent(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: adresse
-- ============================================================================
CREATE TABLE adresse (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_nation INT NOT NULL,
    province_etat VARCHAR(100),
    ville VARCHAR(100),
    commune VARCHAR(100),
    adresse_complete TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_nation) REFERENCES nation(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: contact
-- ============================================================================
CREATE TABLE contact (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tel1 VARCHAR(20),
    tel2 VARCHAR(20),
    whatsapp VARCHAR(20),
    email VARCHAR(100),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: fidele_type
-- Description: Types de fidèles (Pratiquant, Sympathisant)
-- ============================================================================
CREATE TABLE fidele_type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: grade
-- Description: Grades ecclésiastiques
-- ============================================================================
CREATE TABLE grade (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: fidele
-- ============================================================================
CREATE TABLE fidele (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    postnom VARCHAR(100),
    prenom VARCHAR(100) NOT NULL,
    date_naissance DATE,
    numero_carte VARCHAR(50),
    id_grade INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_grade) REFERENCES grade(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: fidele_type_relation
-- Description: Relation Many-to-Many entre fidèles et types de fidèles
-- ============================================================================
CREATE TABLE fidele_type_relation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_fidele INT NOT NULL,
    id_fidele_type INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_fidele) REFERENCES fidele(id) ON DELETE CASCADE,
    FOREIGN KEY (id_fidele_type) REFERENCES fidele_type(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: echellon_eclesiastique
-- Description: Niveaux hiérarchiques (Continent, Nation, Province/État, Ville, Paroisse)
-- ============================================================================
CREATE TABLE echellon_eclesiastique (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    id_echellon_parent INT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_echellon_parent) REFERENCES echellon_eclesiastique(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: structure_type
-- Description: Types de structures (Mouvement, Association, Regroupement)
-- ============================================================================
CREATE TABLE structure_type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: structure_list
-- Description: Liste des structures possibles
-- ============================================================================
CREATE TABLE structure_list (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    id_structure_type INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_structure_type) REFERENCES structure_type(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: structure
-- Description: Instances de structures aux différents échelons
-- ============================================================================
CREATE TABLE structure (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    id_echellon_eclesiastique INT NOT NULL,
    id_line INT NOT NULL COMMENT 'ID du continent, nation, province, ville, ou paroisse',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_echellon_eclesiastique) REFERENCES echellon_eclesiastique(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: fonction_list
-- Description: Liste des fonctions possibles dans les structures
-- ============================================================================
CREATE TABLE fonction_list (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: structure_fonction
-- Description: Attribution de fonctions aux fidèles dans les structures
-- ============================================================================
CREATE TABLE structure_fonction (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_structure INT NOT NULL,
    id_fonction INT NOT NULL,
    id_fidele INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    est_suspendu BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_structure) REFERENCES structure(id) ON DELETE CASCADE,
    FOREIGN KEY (id_fonction) REFERENCES fonction_list(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_fidele) REFERENCES fidele(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INDEX DE PERFORMANCE
-- ============================================================================
CREATE INDEX idx_fidele_nom ON fidele(nom);
CREATE INDEX idx_fidele_grade ON fidele(id_grade);
CREATE INDEX idx_structure_echellon ON structure(id_echellon_eclesiastique);
CREATE INDEX idx_structure_fonction_structure ON structure_fonction(id_structure);
CREATE INDEX idx_structure_fonction_fidele ON structure_fonction(id_fidele);
CREATE INDEX idx_adresse_continent ON adresse(id_continent);
CREATE INDEX idx_adresse_nation ON adresse(id_nation);

-- ============================================================================
-- DONNÉES INITIALES RECOMMANDÉES
-- ============================================================================

-- Continents
INSERT INTO continent (nom) VALUES ('Afrique');
INSERT INTO continent (nom) VALUES ('Amérique du Nord');
INSERT INTO continent (nom) VALUES ('Amérique du Sud');
INSERT INTO continent (nom) VALUES ('Europe');
INSERT INTO continent (nom) VALUES ('Asie');
INSERT INTO continent (nom) VALUES ('Océanie');

-- Types de fidèles
INSERT INTO fidele_type (nom) VALUES ('Pratiquant');
INSERT INTO fidele_type (nom) VALUES ('Sympathisant');

-- Échelons ecclésiastiques (hiérarchie)
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Continent', NULL);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Nation', 1);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Province ou État', 2);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Ville', 3);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Paroisse', 4);

-- Types de structures
INSERT INTO structure_type (nom) VALUES ('Mouvement');
INSERT INTO structure_type (nom) VALUES ('Association');
INSERT INTO structure_type (nom) VALUES ('Regroupement');

-- ============================================================================
-- FIN DU SCRIPT DE CRÉATION
-- ============================================================================

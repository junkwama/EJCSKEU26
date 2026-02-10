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
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL
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
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: document_type
-- Description: Types de documents (FIDELE, PAROISSE, STRUCTURE)
-- ============================================================================
CREATE TABLE document_type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    document_key VARCHAR(50) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: adresse
-- ============================================================================
CREATE TABLE adresse (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_document_type INT NOT NULL,
    id_document INT NOT NULL,
    id_nation INT NOT NULL,
    province_etat VARCHAR(100),
    ville VARCHAR(100),
    commune VARCHAR(100) DEFAULT NULL,
    avenue VARCHAR(100),
    numero VARCHAR(50),
    adresse_complete TEXT DEFAULT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL,
    FOREIGN KEY (id_document_type) REFERENCES document_type(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_nation) REFERENCES nation(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: contact
-- ============================================================================
CREATE TABLE contact (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_document_type INT NOT NULL,
    id_document INT NOT NULL,
    tel1 VARCHAR(20),
    tel2 VARCHAR(20) DEFAULT NULL,
    whatsapp VARCHAR(20) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL,
    FOREIGN KEY (id_document_type) REFERENCES document_type(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: fidele_type
-- Description: Types de fidèles (Pratiquant, Sympathisant)
-- ============================================================================
CREATE TABLE fidele_type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: grade
-- Description: Grades ecclésiastiques
-- ============================================================================
CREATE TABLE grade (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: paroisse
-- Description: Paroisses de l'Église Kimbaguiste
-- ============================================================================
CREATE TABLE paroisse (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: fidele
-- ============================================================================
CREATE TABLE fidele (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    postnom VARCHAR(100),
    prenom VARCHAR(100) NOT NULL,
    sexe CHAR(1) CHECK (sexe IN ('M', 'F')) NOT NULL,
    numero_carte VARCHAR(50) DEFAULT NULL UNIQUE,
    date_naissance DATE,
    est_baptise TINYINT(1),
    date_bapteme DATE DEFAULT NULL,
    id_fidele_type INT,
    id_grade INT,
    id_paroisse INT DEFAULT NULL,
    tel VARCHAR(20),
    password VARCHAR(255) DEFAULT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL,
    FOREIGN KEY (id_grade) REFERENCES grade(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_fidele_type) REFERENCES fidele_type(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_paroisse) REFERENCES paroisse(id) ON DELETE SET NULL
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
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL,
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
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL
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
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL,
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
    id_adresse INT,
    id_contact INT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL,
    FOREIGN KEY (id_echellon_eclesiastique) REFERENCES echellon_eclesiastique(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_adresse) REFERENCES adresse(id) ON DELETE SET NULL,
    FOREIGN KEY (id_contact) REFERENCES contact(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: fonction_list
-- Description: Liste des fonctions possibles dans les structures
-- ============================================================================
CREATE TABLE fonction_list (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL
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
    est_supprimee BOOLEAN DEFAULT FALSE,
    date_suppression TIMESTAMP NULL,
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
CREATE INDEX idx_adresse_nation ON adresse(id_nation);
CREATE INDEX idx_adresse_document ON adresse(id_document_type, id_document);
CREATE INDEX idx_contact_document ON contact(id_document_type, id_document);
CREATE INDEX idx_fidele_est_supprimee ON fidele(est_supprimee);
CREATE INDEX idx_structure_est_supprimee ON structure(est_supprimee);
CREATE INDEX idx_contact_est_supprimee ON contact(est_supprimee);
CREATE INDEX idx_adresse_est_supprimee ON adresse(est_supprimee);

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

-- Nations (triées alphabétiquement - de l'Afghanistan au Zimbabwe)
INSERT INTO nation (nom, id_continent) VALUES ('Afghanistan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Afrique du Sud', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Albanie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Algérie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Allemagne', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Andorre', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Angola', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Antigua-et-Barbuda', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Arabie Saoudite', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Arménie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Australie', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Autriche', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Azerbaïdjan', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Bahamas', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Bahreïn', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Bangladesh', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Barbade', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Belgique', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Belize', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Bénin', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Bhoutan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Biélorussie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Birmanie', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Bolivie', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Bosnie-Herzégovine', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Botswana', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Brésil', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Brunei', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Bulgarie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Burkina Faso', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Burundi', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Cambodge', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Cameroun', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Canada', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Cap-Vert', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Chili', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Chine', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Chypre', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Chypre du Nord', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Colombie', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Comores', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Congo', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Corée du Nord', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Corée du Sud', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Costa Rica', 2);
INSERT INTO nation (nom, id_continent) VALUES ("Côte d'Ivoire", 1);
INSERT INTO nation (nom, id_continent) VALUES ('Croatie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Cuba', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Danemark', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Djibouti', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Dominique', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Égypte', 1);
INSERT INTO nation (nom, id_continent) VALUES ('El Salvador', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Émirats Arabes Unis', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Équateur', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Érythrée', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Espagne', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Estonie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Eswatini', 1);
INSERT INTO nation (nom, id_continent) VALUES ('États-Unis', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Éthiopie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Fidji', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Finlande', 4);
INSERT INTO nation (nom, id_continent) VALUES ('France', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Gabon', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Gambie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Géorgie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Géorgie du Sud-Ossétie', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Ghana', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Gibraltar', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Grèce', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Grenade', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Groenland', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Guadeloupe', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Guam', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Guatemala', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Guernesey', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Guinée', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Guinée équatoriale', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Guinée-Bissau', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Guyana', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Guyane française', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Haïti', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Honduras', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Hong Kong', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Hongrie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Île Bouvet', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Île Christmas', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Île Norfolk', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Îles Åland', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Îles Féroé', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Îles Heard et MacDonald', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Îles Mariannes du Nord', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Îles Pitcairn', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Inde', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Indonésie', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Irak', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Iran', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Irlande', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Islande', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Israël', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Italie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Jamaïque', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Japon', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Jersey', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Jordanie', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Kazakhstan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Kenya', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Kirghizistan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Kiribati', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Kosovo', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Koweït', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Laos', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Lesotho', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Lettonie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Liban', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Liberia', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Libye', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Liechtenstein', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Lituanie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Luxembourg', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Macao', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Macédoine du Nord', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Madagascar', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Malaisie', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Malawi', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Maldives', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Mali', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Malte', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Maroc', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Martinique', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Maurice', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Mauritanie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Mayotte', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Mexique', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Micronésie', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Moldavie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Mongolie', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Monténégro', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Montserrat', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Mozambique', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Namibie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Nauru', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Népal', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Nicaragua', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Niger', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Nigeria', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Niue', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Norvège', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Nouvelle-Calédonie', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Nouvelle-Zélande', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Oman', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Ouganda', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Ouzbékistan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Palaos', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Palestine', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Panama', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Papouasie-Nouvelle-Guinée', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Pakistan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Paraguay', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Pays-Bas', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Pérou', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Philippines', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Pologne', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Polynésie française', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Porto Rico', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Portugal', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Qatar', 5);
INSERT INTO nation (nom, id_continent) VALUES ('République Centrafricaine', 1);
INSERT INTO nation (nom, id_continent) VALUES ('République Démocratique du Congo', 1);
INSERT INTO nation (nom, id_continent) VALUES ('République Dominicaine', 2);
INSERT INTO nation (nom, id_continent) VALUES ('République Tchèque', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Réunion', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Roumanie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Royaume-Uni', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Russie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Rwanda', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Sahara occidental', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Saint-Barthélemy', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Sainte-Hélène', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Sainte-Lucie', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Saint-Marin', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Saint-Martin', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Saint-Pierre-et-Miquelon', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Saint-Vincent-et-les-Grenadines', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Saint-Christophe-et-Niévès', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Samoa', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Samoa américaines', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Sao Tomé-et-Principe', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Sénégal', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Serbie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Seychelles', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Sierra Leone', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Singapour', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Sint Maarten', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Slovaquie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Slovénie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Somalie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Soudan', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Soudan du Sud', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Sri Lanka', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Suède', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Suisse', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Suriname', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Svalbard et Jan Mayen', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Syrie', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Tadjikistan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Taïwan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Tanzanie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Tchad', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Terres australes françaises', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Territoire britannique de l''océan Indien', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Thaïlande', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Timor oriental', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Togo', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Tokelau', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Tonga', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Trinité-et-Tobago', 2);
INSERT INTO nation (nom, id_continent) VALUES ('Tunisie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Turkménistan', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Turquie', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Tuvalu', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Ukraine', 4);
INSERT INTO nation (nom, id_continent) VALUES ('Uruguay', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Vanuatu', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Vénézuela', 3);
INSERT INTO nation (nom, id_continent) VALUES ('Viêt Nam', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Wallis-et-Futuna', 6);
INSERT INTO nation (nom, id_continent) VALUES ('Yémen', 5);
INSERT INTO nation (nom, id_continent) VALUES ('Zambie', 1);
INSERT INTO nation (nom, id_continent) VALUES ('Zimbabwe', 1);

-- Types de fidèles
INSERT INTO fidele_type (nom) VALUES ('Pratiquant');
INSERT INTO fidele_type (nom) VALUES ('Sympathisant');

-- Grades ecclésiastiques
INSERT INTO grade (nom) VALUES ('Mondimi');
INSERT INTO grade (nom) VALUES ('Nkengi');
INSERT INTO grade (nom) VALUES ('Longi');
INSERT INTO grade (nom) VALUES ('Sielo');
INSERT INTO grade (nom) VALUES ('Pasteur');

-- Fonctions
INSERT INTO fonction_list (nom) VALUES ('Pasteur Responsable');
INSERT INTO fonction_list (nom) VALUES ('Pasteur évangéliste');
INSERT INTO fonction_list (nom) VALUES ('Sielo responsable');
INSERT INTO fonction_list (nom) VALUES ('Président');
INSERT INTO fonction_list (nom) VALUES ('Vice Président');
INSERT INTO fonction_list (nom) VALUES ('Secrétaire');
INSERT INTO fonction_list (nom) VALUES ('Secrétaire adjoint');
INSERT INTO fonction_list (nom) VALUES ('Trésorier');
INSERT INTO fonction_list (nom) VALUES ('Trésorier adjoint');
INSERT INTO fonction_list (nom) VALUES ('Conseiller');
INSERT INTO fonction_list (nom) VALUES ('Dirigeant technique');
INSERT INTO fonction_list (nom) VALUES ('Chef de cellule');
INSERT INTO fonction_list (nom) VALUES ('Chef de partition');

-- Échelons ecclésiastiques (hiérarchie)
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Général', NULL);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Continent', 1);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Nation', 2);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Province ou État', 3);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Ville', 4);
INSERT INTO echellon_eclesiastique (nom, id_echellon_parent) VALUES ('Paroisse', 5);
-- Types de structures
INSERT INTO structure_type (nom) VALUES ('Mouvement');
INSERT INTO structure_type (nom) VALUES ('Association');
INSERT INTO structure_type (nom) VALUES ('Regroupement');

-- Document types
INSERT INTO document_type (nom, Document_key) VALUES ('FIDELE', 'FIDELE');
INSERT INTO document_type (nom, Document_key) VALUES ('PAROISSE', 'PAROISSE');
INSERT INTO document_type (nom, Document_key) VALUES ('STRUCTURE', 'STRUCTURE');

-- ============================================================================
-- FIN DU SCRIPT DE CRÉATION
-- ============================================================================

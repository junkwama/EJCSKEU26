-- Seed data migrated from db.sql (idempotent-ish).
-- NOTE: Avoid DROP/CREATE DATABASE here.

-- Continents (IDs not used by enums; set explicitly for stable FK in nations)
INSERT IGNORE INTO continent (id, nom) VALUES
  (1, 'Afrique'),
  (2, 'Amérique du Nord'),
  (3, 'Amérique du Sud'),
  (4, 'Europe'),
  (5, 'Asie'),
  (6, 'Océanie');

-- Nations (keep as INSERT IGNORE to avoid duplicates)
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Afghanistan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Afrique du Sud', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Albanie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Algérie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Allemagne', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Andorre', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Angola', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Antigua-et-Barbuda', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Arabie Saoudite', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Arménie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Australie', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Autriche', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Azerbaïdjan', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bahamas', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bahreïn', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bangladesh', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Barbade', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Belgique', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Belize', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bénin', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bhoutan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Biélorussie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Birmanie', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bolivie', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bosnie-Herzégovine', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Botswana', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Brésil', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Brunei', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Bulgarie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Burkina Faso', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Burundi', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Cambodge', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Cameroun', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Canada', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Cap-Vert', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Chili', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Chine', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Chypre', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Chypre du Nord', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Colombie', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Comores', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Congo', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Corée du Nord', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Corée du Sud', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Costa Rica', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Côte d''Ivoire', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Croatie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Cuba', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Danemark', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Djibouti', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Dominique', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Égypte', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('El Salvador', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Émirats Arabes Unis', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Équateur', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Érythrée', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Espagne', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Estonie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Eswatini', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('États-Unis', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Éthiopie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Fidji', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Finlande', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('France', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Gabon', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Gambie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Géorgie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Géorgie du Sud-Ossétie', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Ghana', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Gibraltar', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Grèce', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Grenade', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Groenland', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guadeloupe', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guam', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guatemala', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guernesey', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guinée', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guinée équatoriale', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guinée-Bissau', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guyana', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Guyane française', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Haïti', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Honduras', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Hong Kong', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Hongrie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Île Bouvet', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Île Christmas', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Île Norfolk', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Îles Åland', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Îles Féroé', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Îles Heard et MacDonald', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Îles Mariannes du Nord', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Îles Pitcairn', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Inde', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Indonésie', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Irak', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Iran', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Irlande', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Islande', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Israël', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Italie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Jamaïque', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Japon', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Jersey', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Jordanie', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Kazakhstan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Kenya', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Kirghizistan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Kiribati', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Kosovo', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Koweït', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Laos', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Lesotho', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Lettonie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Liban', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Liberia', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Libye', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Liechtenstein', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Lituanie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Luxembourg', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Macao', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Macédoine du Nord', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Madagascar', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Malaisie', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Malawi', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Maldives', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Mali', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Malte', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Maroc', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Martinique', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Maurice', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Mauritanie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Mayotte', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Mexique', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Micronésie', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Moldavie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Mongolie', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Monténégro', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Montserrat', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Mozambique', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Namibie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Nauru', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Népal', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Nicaragua', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Niger', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Nigeria', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Niue', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Norvège', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Nouvelle-Calédonie', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Nouvelle-Zélande', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Oman', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Ouganda', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Ouzbékistan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Palaos', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Palestine', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Panama', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Papouasie-Nouvelle-Guinée', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Pakistan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Paraguay', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Pays-Bas', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Pérou', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Philippines', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Pologne', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Polynésie française', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Porto Rico', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Portugal', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Qatar', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('République Centrafricaine', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('République Démocratique du Congo', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('République Dominicaine', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('République Tchèque', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Réunion', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Roumanie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Royaume-Uni', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Russie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Rwanda', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sahara occidental', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Saint-Barthélemy', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sainte-Hélène', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sainte-Lucie', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Saint-Marin', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Saint-Martin', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Saint-Pierre-et-Miquelon', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Saint-Vincent-et-les-Grenadines', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Saint-Christophe-et-Niévès', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Samoa', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Samoa américaines', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sao Tomé-et-Principe', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sénégal', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Serbie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Seychelles', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sierra Leone', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Singapour', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sint Maarten', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Slovaquie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Slovénie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Somalie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Soudan', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Soudan du Sud', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Sri Lanka', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Suède', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Suisse', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Suriname', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Svalbard et Jan Mayen', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Syrie', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Tadjikistan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Taïwan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Tanzanie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Tchad', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Terres australes françaises', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Territoire britannique de l''océan Indien', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Thaïlande', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Timor oriental', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Togo', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Tokelau', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Tonga', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Trinité-et-Tobago', 2);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Tunisie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Turkménistan', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Turquie', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Tuvalu', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Ukraine', 4);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Uruguay', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Vanuatu', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Vénézuela', 3);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Viêt Nam', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Wallis-et-Futuna', 6);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Yémen', 5);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Zambie', 1);
INSERT IGNORE INTO nation (nom, id_continent) VALUES ('Zimbabwe', 1);

-- Structure types (IDs fixed to match StructureTypeEnum)
INSERT IGNORE INTO structure_type (id, nom) VALUES
  (1, 'Direction Ecclésiastique'),
  (2, 'Mouvement'),
  (3, 'Association'),
  (4, 'Service');

-- Bureau structure (ensure at least one exists)
INSERT INTO structure (nom, code, description, id_structure_type)
SELECT
  'Bureau Ecclésiastique',
  'BUREAU_ECCLESIASTIQUE',
  'Organe chargé de l’administration des fidèles à un échelon géographique donné (paroissial, provincial, national, etc.)',
  1
WHERE NOT EXISTS (
  SELECT 1 FROM structure WHERE code = 'BUREAU_ECCLESIASTIQUE'
);

-- Fidele types (IDs fixed to match FideleTypeEnum)
INSERT IGNORE INTO fidele_type (id, nom) VALUES
  (1, 'Pratiquant'),
  (2, 'Sympathisant');

-- Grades (IDs fixed to match GradeEnum)
INSERT IGNORE INTO grade (id, nom) VALUES
  (1, 'Mondimi'),
  (2, 'Nkengi'),
  (3, 'Longi'),
  (4, 'Sielo'),
  (5, 'Pasteur');

-- Fonctions (idempotent even if nom isn't UNIQUE)
INSERT INTO fonction_list (nom)
SELECT 'Pasteur Responsable' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Pasteur Responsable');
INSERT INTO fonction_list (nom)
SELECT 'Pasteur évangéliste' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Pasteur évangéliste');
INSERT INTO fonction_list (nom)
SELECT 'Sielo responsable' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Sielo responsable');
INSERT INTO fonction_list (nom)
SELECT 'Président' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Président');
INSERT INTO fonction_list (nom)
SELECT 'Vice Président' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Vice Président');
INSERT INTO fonction_list (nom)
SELECT 'Secrétaire' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Secrétaire');
INSERT INTO fonction_list (nom)
SELECT 'Secrétaire adjoint' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Secrétaire adjoint');
INSERT INTO fonction_list (nom)
SELECT 'Trésorier' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Trésorier');
INSERT INTO fonction_list (nom)
SELECT 'Trésorier adjoint' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Trésorier adjoint');
INSERT INTO fonction_list (nom)
SELECT 'Conseiller' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Conseiller');
INSERT INTO fonction_list (nom)
SELECT 'Dirigeant technique' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Dirigeant technique');
INSERT INTO fonction_list (nom)
SELECT 'Chef de cellule' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Chef de cellule');
INSERT INTO fonction_list (nom)
SELECT 'Chef de partition' WHERE NOT EXISTS (SELECT 1 FROM fonction_list WHERE nom='Chef de partition');

-- Document types (IDs fixed to match DocumentTypeEnum)
INSERT IGNORE INTO document_type (id, nom, document_key) VALUES
  (1, 'FIDELE', 'FIDELE'),
  (2, 'STRUCTURE', 'STRUCTURE'),
  (3, 'PAROISSE', 'PAROISSE'),
  (4, 'VILLE', 'VILLE'),
  (5, 'PROVINCE', 'PROVINCE'),
  (6, 'NATION', 'NATION'),
  (7, 'CONTINENT', 'CONTINENT'),
  (8, 'GENERALE', 'GENERALE');

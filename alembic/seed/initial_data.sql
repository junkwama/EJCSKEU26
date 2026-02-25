-- Seed data migrated from db.sql (idempotent-ish).
-- NOTE: Avoid DROP/CREATE DATABASE here.

-- Continents (IDs not used by enums; set explicitly for stable FK in nations)
INSERT INTO continent (id, nom) VALUES
  (1, 'Afrique'),
  (2, 'Amérique du Nord'),
  (3, 'Amérique du Sud'),
  (4, 'Europe'),
  (5, 'Asie'),
  (6, 'Océanie');

-- Nations (base courante; ISO codes added in later migration)
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Afghanistan', 5, 'AF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Afrique du Sud', 1, 'ZA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Albanie', 4, 'AL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Algérie', 1, 'DZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Allemagne', 4, 'DE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Andorre', 4, 'AD');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Angola', 1, 'AO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Antigua-et-Barbuda', 2, 'AG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Arabie Saoudite', 5, 'SA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Arménie', 4, 'AM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Australie', 6, 'AU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Autriche', 4, 'AT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Azerbaïdjan', 4, 'AZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bahamas', 2, 'BS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bahreïn', 5, 'BH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bangladesh', 5, 'BD');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Barbade', 2, 'BB');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Belgique', 4, 'BE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Belize', 2, 'BZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bénin', 1, 'BJ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bhoutan', 5, 'BT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Biélorussie', 4, 'BY');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Birmanie', 5, 'MM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bolivie', 3, 'BO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bosnie-Herzégovine', 4, 'BA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Botswana', 1, 'BW');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Brésil', 3, 'BR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Brunei', 5, 'BN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Bulgarie', 4, 'BG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Burkina Faso', 1, 'BF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Burundi', 1, 'BI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Cambodge', 5, 'KH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Cameroun', 1, 'CM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Canada', 2, 'CA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Cap-Vert', 1, 'CV');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Chili', 3, 'CL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Chine', 5, 'CN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Chypre', 4, 'CY');
-- INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Chypre du Nord', 5, 'NULL'); -- No ISO Code
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Colombie', 3, 'CO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Comores', 1, 'KM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Congo', 1, 'CG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Corée du Nord', 5, 'KP');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Corée du Sud', 5, 'KR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Costa Rica', 2, 'CR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Côte d''Ivoire', 1, 'CI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Croatie', 4, 'HR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Cuba', 2, 'CU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Danemark', 4, 'DK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Djibouti', 1, 'DJ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Dominique', 2, 'DM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Égypte', 1, 'EG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('El Salvador', 2, 'SV');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Émirats Arabes Unis', 5, 'AE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Équateur', 3, 'EC');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Érythrée', 1, 'ER');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Espagne', 4, 'ES');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Estonie', 4, 'EE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Eswatini', 1, 'SZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('États-Unis', 2, 'US');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Éthiopie', 1, 'ET');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Fidji', 6, 'FJ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Finlande', 4, 'FI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('France', 4, 'FR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Gabon', 1, 'GA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Gambie', 1, 'GM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Géorgie', 4, 'GE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Géorgie du Sud-Ossétie', 5, 'GS'); -- Corrected to South Georgia code (GS)
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Ghana', 1, 'GH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Gibraltar', 4, 'GI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Grèce', 4, 'GR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Grenade', 2, 'GD');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Groenland', 4, 'GL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guadeloupe', 2, 'GP');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guam', 6, 'GU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guatemala', 2, 'GT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guernesey', 4, 'GG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guinée', 1, 'GN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guinée équatoriale', 1, 'GQ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guinée-Bissau', 1, 'GW');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guyana', 3, 'GY');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Guyane française', 3, 'GF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Haïti', 2, 'HT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Honduras', 2, 'HN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Hong Kong', 5, 'HK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Hongrie', 4, 'HU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Île Bouvet', 4, 'BV');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Île Christmas', 6, 'CX');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Île Norfolk', 6, 'NF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Îles Åland', 4, 'AX');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Îles Féroé', 4, 'FO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Îles Heard et MacDonald', 6, 'HM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Îles Mariannes du Nord', 6, 'MP');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Îles Pitcairn', 6, 'PN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Inde', 5, 'IN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Indonésie', 5, 'ID');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Irak', 5, 'IQ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Iran', 5, 'IR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Irlande', 4, 'IE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Islande', 4, 'IS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Israël', 5, 'IL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Italie', 4, 'IT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Jamaïque', 2, 'JM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Japon', 5, 'JP');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Jersey', 4, 'JE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Jordanie', 5, 'JO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Kazakhstan', 5, 'KZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Kenya', 1, 'KE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Kirghizistan', 5, 'KG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Kiribati', 6, 'KI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Kosovo', 4, 'XK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Koweït', 5, 'KW');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Laos', 5, 'LA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Lesotho', 1, 'LS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Lettonie', 4, 'LV');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Liban', 5, 'LB');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Liberia', 1, 'LR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Libye', 1, 'LY');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Liechtenstein', 4, 'LI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Lituanie', 4, 'LT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Luxembourg', 4, 'LU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Macao', 5, 'MO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Macédoine du Nord', 4, 'MK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Madagascar', 1, 'MG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Malaisie', 5, 'MY');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Malawi', 1, 'MW');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Maldives', 5, 'MV');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Mali', 1, 'ML');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Malte', 4, 'MT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Maroc', 1, 'MA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Martinique', 2, 'MQ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Maurice', 1, 'MU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Mauritanie', 1, 'MR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Mayotte', 1, 'YT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Mexique', 2, 'MX');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Micronésie', 6, 'FM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Moldavie', 4, 'MD');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Mongolie', 5, 'MN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Monténégro', 4, 'ME');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Montserrat', 2, 'MS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Mozambique', 1, 'MZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Namibie', 1, 'NA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Nauru', 6, 'NR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Népal', 5, 'NP');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Nicaragua', 2, 'NI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Niger', 1, 'NE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Nigeria', 1, 'NG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Niue', 6, 'NU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Norvège', 4, 'NO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Nouvelle-Calédonie', 6, 'NC');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Nouvelle-Zélande', 6, 'NZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Oman', 5, 'OM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Ouganda', 1, 'UG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Ouzbékistan', 5, 'UZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Palaos', 6, 'PW');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Palestine', 5, 'PS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Panama', 2, 'PA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Papouasie-Nouvelle-Guinée', 6, 'PG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Pakistan', 5, 'PK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Paraguay', 3, 'PY');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Pays-Bas', 4, 'NL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Pérou', 3, 'PE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Philippines', 5, 'PH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Pologne', 4, 'PL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Polynésie française', 6, 'PF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Porto Rico', 2, 'PR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Portugal', 4, 'PT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Qatar', 5, 'QA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('République Centrafricaine', 1, 'CF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('République Démocratique du Congo', 1, 'CD');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('République Dominicaine', 2, 'DO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('République Tchèque', 4, 'CZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Réunion', 1, 'RE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Roumanie', 4, 'RO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Royaume-Uni', 4, 'GB');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Russie', 4, 'RU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Rwanda', 1, 'RW');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sahara occidental', 1, 'EH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Saint-Barthélemy', 2, 'BL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sainte-Hélène', 1, 'SH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sainte-Lucie', 2, 'LC');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Saint-Marin', 2, 'SM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Saint-Martin', 2, 'MF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Saint-Pierre-et-Miquelon', 2, 'PM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Saint-Vincent-et-les-Grenadines', 2, 'VC');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Saint-Christophe-et-Niévès', 2, 'KN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Samoa', 6, 'WS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Samoa américaines', 6, 'AS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sao Tomé-et-Principe', 1, 'ST');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sénégal', 1, 'SN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Serbie', 4, 'RS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Seychelles', 1, 'SC');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sierra Leone', 1, 'SL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Singapour', 5, 'SG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sint Maarten', 2, 'SX');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Slovaquie', 4, 'SK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Slovénie', 4, 'SI');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Somalie', 1, 'SO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Soudan', 1, 'SD');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Soudan du Sud', 1, 'SS');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Sri Lanka', 5, 'LK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Suède', 4, 'SE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Suisse', 4, 'CH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Suriname', 3, 'SR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Svalbard et Jan Mayen', 4, 'SJ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Syrie', 5, 'SY');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Tadjikistan', 5, 'TJ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Taïwan', 5, 'TW');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Tanzanie', 1, 'TZ');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Tchad', 1, 'TD');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Terres australes françaises', 6, 'TF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Territoire britannique de l''océan Indien', 6, 'IO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Thaïlande', 5, 'TH');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Timor oriental', 5, 'TL');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Togo', 1, 'TG');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Tokelau', 6, 'TK');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Tonga', 6, 'TO');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Trinité-et-Tobago', 2, 'TT');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Tunisie', 1, 'TN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Turkménistan', 5, 'TM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Turquie', 4, 'TR');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Tuvalu', 6, 'TV');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Ukraine', 4, 'UA');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Uruguay', 3, 'UY');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Vanuatu', 6, 'VU');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Vénézuela', 3, 'VE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Viêt Nam', 5, 'VN');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Wallis-et-Futuna', 6, 'WF');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Yémen', 5, 'YE');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Zambie', 1, 'ZM');
INSERT INTO nation (nom, id_continent, iso_alpha_2) VALUES ('Zimbabwe', 1, 'ZW');

-- Structure types (IDs fixed to match StructureTypeEnum)
INSERT INTO structure_type (id, nom) VALUES
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
INSERT INTO fidele_type (id, nom) VALUES
  (1, 'Pratiquant'),
  (2, 'Sympathisant');

-- Grades (IDs fixed to match GradeEnum)
INSERT INTO grade (id, nom) VALUES
  (1, 'Mondimi'),
  (2, 'Nkengi'),
  (3, 'Longi'),
  (4, 'Sielo'),
  (5, 'Pasteur');

-- Professions (common values; first one must be Eleve/Etudiant)
INSERT INTO profession (id, nom, description) VALUES
  (1, 'Eleve/Etudiant', 'En formation scolaire ou universitaire'),
  (2, 'Fonctionnaire', 'Agent de l''administration publique'),
  (3, 'Enseignant', 'Profession de l''enseignement'),
  (4, 'Commerçant', 'Activité commerciale indépendante ou structurée'),
  (5, 'Entrepreneur', 'Créateur ou gestionnaire d''entreprise'),
  (6, 'Artisan', 'Métier manuel qualifié'),
  (7, 'Agriculteur', 'Activité agricole et/ou élevage'),
  (8, 'Avocat', 'Profession juridique'),
  (9, 'Médecin', 'Profession médicale'),
  (10, 'Infirmier', 'Profession des soins infirmiers'),
  (11, 'Pharmacien', 'Profession de pharmacie'),
  (12, 'Ingénieur', 'Profession de l''ingénierie'),
  (13, 'Informaticien', 'Profession des systèmes informatiques et numériques'),
  (14, 'Comptable', 'Gestion comptable et financière'),
  (15, 'Banquier', 'Secteur bancaire et services financiers'),
  (16, 'Journaliste', 'Profession des médias et de l''information'),
  (17, 'Chauffeur', 'Transport de personnes ou de marchandises'),
  (18, 'Mécanicien', 'Maintenance et réparation mécanique'),
  (19, 'Électricien', 'Installation et maintenance électrique'),
  (20, 'Maçon', 'Travaux de construction'),
  (21, 'Menuisier', 'Travaux de menuiserie'),
  (22, 'Couturier', 'Confection et couture'),
  (23, 'Coiffeur', 'Soins capillaires et coiffure'),
  (24, 'Militaire', 'Forces armées'),
  (25, 'Policier', 'Forces de l''ordre et sécurité publique'),
  (26, 'Retraité', 'Ancien professionnel en retraite'),
  (27, 'Sans emploi', 'Actuellement sans activité professionnelle'),
  (28, 'Autre', 'Profession non presente sur la liste.');

-- Niveaux d'études (base courante)
INSERT INTO niveau_etudes (id, nom, description) VALUES
  (1, 'Aucun', 'Sans niveau scolaire formel'),
  (2, 'Primaire', 'Niveau d''enseignement primaire'),
  (3, 'Secondaire', 'Niveau d''enseignement secondaire'),
  (4, 'Technique/Professionnel', 'Formation technique ou professionnelle'),
  (5, 'Universitaire', 'Niveau licence/master/doctorat');

-- États civils de base
INSERT INTO etat_civile (id, nom, description) VALUES
  (1, 'Célibataire', 'Personne non mariée'),
  (2, 'Marié', 'Personne mariée'),
  (3, 'Divorcé', 'Personne divorcée'),
  (4, 'Veuf', 'Conjoint décédé');

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
INSERT INTO document_type (id, nom, document_key, code) VALUES
  (1, 'FIDELE', 'FIDELE', 'FDL'),
  (2, 'STRUCTURE', 'STRUCTURE', 'STR'),
  (3, 'PAROISSE', 'PAROISSE', 'PRS'),
  (4, 'VILLE', 'VILLE', 'VLL'),
  (5, 'PROVINCE', 'PROVINCE', 'PRV'),
  (6, 'NATION', 'NATION', 'NTN'),
  (7, 'CONTINENT', 'CONTINENT', 'CTN'),
  (8, 'GENERALE', 'GENERALE', 'GNR');

-- Backfill/align codes for existing rows
UPDATE document_type SET code = 'FDL' WHERE id = 1;
UPDATE document_type SET code = 'STR' WHERE id = 2;
UPDATE document_type SET code = 'PRS' WHERE id = 3;
UPDATE document_type SET code = 'VLL' WHERE id = 4;
UPDATE document_type SET code = 'PRV' WHERE id = 5;
UPDATE document_type SET code = 'NTN' WHERE id = 6;
UPDATE document_type SET code = 'CTN' WHERE id = 7;
UPDATE document_type SET code = 'GNR' WHERE id = 8;

-- Document statuts
INSERT INTO document_statut (id, nom, description, id_document_type) VALUES
  (1, 'En attente', 'Document en attente de traitement/validation', NULL),
  (29, 'Validé', 'Document validé', NULL);

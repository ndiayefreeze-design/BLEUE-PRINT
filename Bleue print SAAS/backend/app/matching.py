from dataclasses import dataclass, field
import csv
from difflib import SequenceMatcher
import os
import re
import unicodedata
from pathlib import Path
from typing import TypedDict

try:
    import psycopg
except Exception:  # pragma: no cover - optional at runtime when DB is unavailable
    psycopg = None

LEGAL_NOTE = "Estimation à titre indicatif — la classification tarifaire officielle et la déclaration en douane relèvent exclusivement d'un commissionnaire en douane agréé via GAINDE."


class CandidateCatalogItem(TypedDict):
    code_sh: str
    libelle: str
    keywords: list[str]
    category_aliases: list[str]
    negative_context: list[str]


class CandidateScore(TypedDict):
    code_sh: str
    libelle: str
    score: float
    reason: str


class GlobalHsRow(TypedDict, total=False):
    code_sh: str
    description_en: str
    description_fr_a_completer: str


NOISE_WORDS = {
    "mot", "mots", "word", "words", "unknown", "unknow", "inconnu", "inconnue", "inconnus", "inconnues",
    "objet", "objets", "article", "articles", "produit", "produits", "item", "items", "type", "types",
    "generic", "generique", "generiques", "specific", "specifique", "specifiques", "particulier",
    "particuliere", "particuliers", "particulieres", "autre", "autres", "divers", "diverse", "diverses",
    "label", "labels", "libelle", "libellé", "description", "descriptions", "argument", "arguments",
    "data", "donnee", "donnees", "donnée", "données", "value", "values", "test", "tests", "sample",
    "samples", "example", "examples", "placeholder", "placeholders", "undefined", "null", "none",
}

CANDIDATE_CODES: list[CandidateCatalogItem] = [
    {
        "code_sh": "8504",
        "libelle": "Chargeurs et adaptateurs électriques; transformateurs électriques",
        "keywords": ["chargeur", "adaptateur", "transformateur", "telephone", "smartphone", "usb", "cable", "telephone", "portable"],
        "category_aliases": ["electronique", "electrique", "technique"],
    },
    {
        "code_sh": "1701",
        "libelle": "Sucres de canne ou de betterave",
        "keywords": ["sucre", "sugar", "canne", "betterave", "sucres"],
        "category_aliases": ["sucre", "agroalimentaire", "alimentaire"],
    },
    {
        "code_sh": "0902",
        "libelle": "Thé, même aromatisé",
        "keywords": ["the", "tea", "infusion", "theiere"],
        "category_aliases": ["boisson", "alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "1101",
        "libelle": "Farines de froment ou de méteil",
        "keywords": ["farine", "farines", "flour", "ble", "mouture"],
        "category_aliases": ["alimentaire", "agroalimentaire", "cereale"],
    },
    {
        "code_sh": "1902",
        "libelle": "Pâtes alimentaires, couscous et produits similaires",
        "keywords": ["pates", "pasta", "spaghetti", "macaroni", "nouilles", "couscous", "semoule"],
        "category_aliases": ["alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "1905",
        "libelle": "Produits de la boulangerie, pâtisserie ou biscuiterie",
        "keywords": ["pain", "biscuit", "biscuits", "gateau", "gateaux", "patisserie", "boulangerie"],
        "category_aliases": ["alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "1511",
        "libelle": "Huile de palme et ses fractions",
        "keywords": ["palme", "huile-palme", "huile_rouge", "palm"],
        "category_aliases": ["alimentaire", "agroalimentaire", "huile"],
    },
    {
        "code_sh": "1604",
        "libelle": "Préparations et conserves de poissons",
        "keywords": ["sardine", "sardines", "thon", "poisson", "poissons", "conserve", "conserves"],
        "category_aliases": ["alimentaire", "agroalimentaire", "peche"],
    },
    {
        "code_sh": "1806",
        "libelle": "Chocolat et autres préparations alimentaires contenant du cacao",
        "keywords": ["chocolat", "cacao", "chocolate"],
        "category_aliases": ["alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "2009",
        "libelle": "Jus de fruits ou de légumes",
        "keywords": ["jus", "juice", "nectar", "fruit", "fruits", "legume", "legumes"],
        "category_aliases": ["boisson", "alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "2201",
        "libelle": "Eaux minérales, eaux gazéifiées et autres eaux",
        "keywords": ["eau-minerale", "eau_minerale", "minerale", "gazeuse", "source"],
        "category_aliases": ["boisson", "alimentaire"],
    },
    {
        "code_sh": "2203",
        "libelle": "Bières de malt",
        "keywords": ["biere", "bieres", "beer", "lager", "brasserie"],
        "category_aliases": ["boisson", "alcool", "agroalimentaire"],
    },
    {
        "code_sh": "2208",
        "libelle": "Alcool éthylique, eaux-de-vie, liqueurs et autres boissons spiritueuses",
        "keywords": ["alcool", "whisky", "rhum", "vodka", "liqueur", "spiritueux", "eau-de-vie"],
        "category_aliases": ["boisson", "alcool"],
    },
    {
        "code_sh": "2710",
        "libelle": "Huiles de pétrole, carburants et lubrifiants",
        "keywords": ["essence", "gasoil", "diesel", "carburant", "kerosene", "lubrifiant", "huile_moteur"],
        "category_aliases": ["energie", "automobile", "transport"],
    },
    {
        "code_sh": "3923",
        "libelle": "Articles pour le transport ou l emballage en matières plastiques",
        "keywords": ["plastique", "plastiques", "sachet", "bouteille", "bidon", "emballage", "barquette", "bouchon"],
        "category_aliases": ["emballage", "plasturgie", "menage"],
    },
    {
        "code_sh": "3924",
        "libelle": "Vaisselle et articles ménagers en matières plastiques",
        "keywords": ["bassine", "seau", "ustensile", "vaisselle", "plastique_menage"],
        "category_aliases": ["menage", "plasturgie"],
    },
    {
        "code_sh": "4819",
        "libelle": "Boîtes, sacs et emballages en papier ou carton",
        "keywords": ["carton", "cartons", "boite", "boites", "enveloppe", "papier", "sachet_papier"],
        "category_aliases": ["emballage", "papeterie"],
    },
    {
        "code_sh": "4901",
        "libelle": "Livres, brochures, prospectus et imprimés similaires",
        "keywords": ["livre", "livres", "brochure", "brochures", "prospectus", "manuel", "catalogue", "imprime"],
        "category_aliases": ["papeterie", "edition"],
    },
    {
        "code_sh": "8415",
        "libelle": "Machines et appareils pour le conditionnement de l air",
        "keywords": ["climatiseur", "climatiseurs", "climatisation", "split", "air_conditionne"],
        "category_aliases": ["electromenager", "climatisation", "confort"],
    },
    {
        "code_sh": "8421",
        "libelle": "Centrifugeuses et appareils pour filtrer ou épurer les liquides ou les gaz",
        "keywords": ["filtre", "filtres", "purificateur", "purificateurs", "filtration", "epuration"],
        "category_aliases": ["traitement_eau", "industrie", "menage"],
    },
    {
        "code_sh": "8528",
        "libelle": "Moniteurs, projecteurs et appareils récepteurs de télévision",
        "keywords": ["television", "televisions", "tv", "ecran", "ecrans", "moniteur", "projecteur", "videoprojecteur"],
        "category_aliases": ["electronique", "audiovisuel"],
    },
    {
        "code_sh": "8541",
        "libelle": "Diodes, dispositifs à semi-conducteurs et cellules photovoltaïques",
        "keywords": ["panneau_solaire", "panneaux", "solaire", "photovoltaique", "led", "diode", "semi-conducteur"],
        "category_aliases": ["electronique", "energie", "solaire"],
    },
    {
        "code_sh": "9018",
        "libelle": "Instruments et appareils pour la médecine, la chirurgie ou l art dentaire",
        "keywords": ["medical", "medicaux", "chirurgical", "chirurgie", "dentaire", "tensiometre", "diagnostic"],
        "category_aliases": ["sante", "medical", "pharmacie"],
    },
    {
        "code_sh": "3003",
        "libelle": "Médicaments non conditionnés pour la vente au détail",
        "keywords": ["medicament_vrac", "substance_pharmaceutique", "principe_actif", "pharmaceutique"],
        "category_aliases": ["pharmacie", "sante", "medical"],
    },
    {
        "code_sh": "3005",
        "libelle": "Ouates, gazes, bandes et articles analogues à usage médical",
        "keywords": ["pansement", "pansements", "compresse", "compresses", "gaze", "bandage", "sparadrap"],
        "category_aliases": ["pharmacie", "sante", "medical"],
    },
    {
        "code_sh": "8518",
        "libelle": "Microphones, haut-parleurs, écouteurs et appareils audio",
        "keywords": ["microphone", "micro", "haut_parleur", "enceinte", "ecouteur", "ecouteurs", "casque_audio", "audio"],
        "category_aliases": ["electronique", "audio", "audiovisuel"],
    },
    {
        "code_sh": "8523",
        "libelle": "Supports pour l enregistrement du son ou de données",
        "keywords": ["disque_dur", "ssd", "cle_usb", "carte_memoire", "memoire", "stockage", "disque"],
        "category_aliases": ["electronique", "informatique", "stockage"],
    },
    {
        "code_sh": "8525",
        "libelle": "Appareils photographiques, caméras et appareils de prise de vues",
        "keywords": ["camera", "cameras", "appareil_photo", "photo", "photos", "video", "videos", "webcam", "drone"],
        "category_aliases": ["electronique", "audiovisuel", "photographie"],
    },
    {
        "code_sh": "8526",
        "libelle": "Appareils de radiodétection, radionavigation et radiotélécommande",
        "keywords": ["gps", "navigation", "radar", "geolocalisation", "telecommande", "drone_navigation"],
        "category_aliases": ["electronique", "navigation", "transport"],
    },
    {
        "code_sh": "9503",
        "libelle": "Jouets, modèles réduits et articles pour jeux",
        "keywords": ["jouet", "jouets", "poupee", "poupees", "puzzle", "jeu", "jeux", "modele_reduit"],
        "category_aliases": ["loisir", "enfant", "sport"],
    },
    {
        "code_sh": "0709",
        "libelle": "Autres légumes, frais ou réfrigérés",
        "keywords": ["legume", "legumes", "manioc", "tomate", "oignon", "pomme_de_terre"],
        "category_aliases": ["agriculture", "alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "0803",
        "libelle": "Bananes, y compris les bananes plantains",
        "keywords": ["banane", "bananes", "plantain", "plantains"],
        "category_aliases": ["agriculture", "alimentaire", "fruits"],
    },
    {
        "code_sh": "0804",
        "libelle": "Dattes, figues, ananas, avocats, goyaves, mangues et mangoustans",
        "keywords": ["mangue", "mangues", "ananas", "datte", "dattes", "avocat", "goyave"],
        "category_aliases": ["agriculture", "alimentaire", "fruits"],
    },
    {
        "code_sh": "0801",
        "libelle": "Noix de coco, noix du Brésil et noix de cajou",
        "keywords": ["cajou", "noix_cajou", "coco", "noix", "amande"],
        "category_aliases": ["agriculture", "alimentaire", "fruits"],
    },
    {
        "code_sh": "1209",
        "libelle": "Graines, fruits et spores à ensemencer",
        "keywords": ["semence", "semences", "graine", "graines", "seed", "plantation", "ensemencement"],
        "category_aliases": ["agriculture", "agronomie", "intrants"],
    },
    {
        "code_sh": "3105",
        "libelle": "Engrais minéraux ou chimiques",
        "keywords": ["engrais", "fertilisant", "fertilisants", "uree", "azote", "phosphate", "potasse", "nkp"],
        "category_aliases": ["agriculture", "agronomie", "intrants"],
    },
    {
        "code_sh": "3808",
        "libelle": "Insecticides, herbicides, fongicides et produits phytosanitaires",
        "keywords": ["pesticide", "pesticides", "herbicide", "herbicides", "fongicide", "insecticide", "phytosanitaire"],
        "category_aliases": ["agriculture", "agronomie", "intrants"],
    },
    {
        "code_sh": "8432",
        "libelle": "Machines et appareils agricoles pour le travail du sol",
        "keywords": ["charrue", "charrues", "semoir", "semoirs", "labour", "cultivateur", "moissonneuse", "agricole"],
        "category_aliases": ["agriculture", "machine_agricole", "agronomie"],
    },
    {
        "code_sh": "8701",
        "libelle": "Tracteurs agricoles et autres tracteurs",
        "keywords": ["tracteur", "tracteurs", "tractor", "motoculteur", "motoculteurs"],
        "category_aliases": ["agriculture", "machine_agricole", "transport"],
    },
    {
        "code_sh": "2309",
        "libelle": "Préparations pour l alimentation des animaux",
        "keywords": ["aliment_animaux", "nourriture_animaux", "provende", "aliment_betail", "croquettes", "fourrage"],
        "category_aliases": ["agriculture", "elevage", "agroalimentaire"],
    },
    {
        "code_sh": "0207",
        "libelle": "Viandes et abats comestibles de volailles",
        "keywords": ["poulet", "poulets", "volaille", "volailles", "viande", "viandes", "abats"],
        "category_aliases": ["elevage", "alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "0401",
        "libelle": "Lait et crème de lait, non concentrés ni additionnés de sucre",
        "keywords": ["lait", "laits", "creme_lait", "produit_laitier", "laitier"],
        "category_aliases": ["elevage", "alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "7308",
        "libelle": "Constructions et parties de constructions en fer ou en acier",
        "keywords": ["charpente", "poutrelle", "structure", "construction_acier", "ossature", "echafaudage", "echafaudages", "echafaudage_metallique"],
        "category_aliases": ["construction", "batiment", "materiaux"],
    },
    {
        "code_sh": "6912",
        "libelle": "Vaisselle et articles de ménage en matières céramiques",
        "keywords": ["ceramique", "ceramiques", "faience", "assiette", "tasse", "bol"],
        "category_aliases": ["menage", "ceramique", "maison"],
    },
    {
        "code_sh": "9404",
        "libelle": "Sommiers, articles de literie et articles similaires",
        "keywords": ["matelas", "sommier", "couette", "oreiller", "coussin", "edredon", "literie"],
        "category_aliases": ["maison", "ameublement", "literie"],
    },
    {
        "code_sh": "8507",
        "libelle": "Accumulateurs électriques et batteries",
        "keywords": ["batterie", "batteries", "accumulateur", "pile", "piles"],
        "category_aliases": ["electronique", "automobile", "energie"],
    },
    {
        "code_sh": "4011",
        "libelle": "Pneumatiques neufs en caoutchouc",
        "keywords": ["pneu", "pneus", "pneumatique", "pneumatiques", "tyre", "tire"],
        "category_aliases": ["automobile", "transport", "mecanique"],
    },
    {
        "code_sh": "1006",
        "libelle": "Riz",
        "keywords": ["riz", "rice"],
        "category_aliases": ["alimentaire", "agroalimentaire", "cereale"],
    },
    {
        "code_sh": "0901",
        "libelle": "Café, même torréfié ou décaféiné",
        "keywords": ["cafe", "coffee"],
        "category_aliases": ["alimentaire", "agroalimentaire", "boisson"],
    },
    {
        "code_sh": "3004",
        "libelle": "Médicaments présentés sous forme de doses ou conditionnés pour la vente au détail",
        "keywords": ["medicament", "medicaments", "medicine", "pharmacie", "pharmaceutical", "comprime", "sirop"],
        "category_aliases": ["pharmacie", "sante", "medical"],
    },
    {
        "code_sh": "3303",
        "libelle": "Parfums, eaux de toilette et préparations de parfumerie",
        "keywords": ["parfum", "parfums", "parfumerie", "fragrance", "eau", "toilette"],
        "category_aliases": ["parfum", "parfumerie", "beaute", "cosmetique"],
    },
    {
        "code_sh": "2202",
        "libelle": "Boissons non alcooliques, eaux et autres boissons",
        "keywords": ["boisson", "boissons", "drink", "drinks", "jus", "soda", "limonade", "eau", "eaux", "rafraichissement"],
        "category_aliases": ["boisson", "boissons", "alimentaire", "agroalimentaire"],
    },
    {
        "code_sh": "7606",
        "libelle": "Tôles et bandes en aluminium",
        "keywords": ["aluminium", "aluminum", "allimunium", "alu", "metal", "tôle", "toles", "bande"],
        "category_aliases": ["aluminium", "metallurgie", "construction", "materiaux"],
    },
    {
        "code_sh": "6403",
        "libelle": "Chaussures à semelles extérieures en caoutchouc, plastique, cuir ou matière textile",
        "keywords": ["chaussure", "chaussures", "shoe", "shoes", "basket", "sandale", "sandales", "botte", "bottes"],
        "category_aliases": ["chaussure", "mode", "habillement"],
    },
    {
        "code_sh": "4202",
        "libelle": "Malles, valises, sacs et contenants similaires",
        "keywords": ["sac", "sacs", "bag", "bags", "valise", "valises", "cartable", "sacoche"],
        "category_aliases": ["maroquinerie", "mode", "accessoire"],
    },
    {
        "code_sh": "8517",
        "libelle": "Téléphones, smartphones et appareils de communication",
        "keywords": ["telephone", "telephones", "smartphone", "smartphones", "mobile", "portable", "iphone", "android"],
        "category_aliases": ["electronique", "telephonie", "communication"],
    },
    {
        "code_sh": "8471",
        "libelle": "Machines automatiques de traitement de l'information et ordinateurs",
        "keywords": ["ordinateur", "ordinateurs", "computer", "computers", "pc", "laptop", "portable", "clavier", "souris"],
        "category_aliases": ["informatique", "electronique", "bureau"],
    },
    {
        "code_sh": "8418",
        "libelle": "Réfrigérateurs, congélateurs et autres appareils frigorifiques",
        "keywords": ["refrigerateur", "refrigerateurs", "frigo", "congelateur", "congelateurs", "freezer"],
        "category_aliases": ["electromenager", "menage", "froid"],
    },
    {
        "code_sh": "8450",
        "libelle": "Machines à laver le linge",
        "keywords": ["lave-linge", "lavelinge", "machine", "laver", "washing", "washing-machine"],
        "category_aliases": ["electromenager", "menage"],
    },
    {
        "code_sh": "8708",
        "libelle": "Parties et accessoires de véhicules automobiles",
        "keywords": ["piece", "pieces", "auto", "automobile", "moteur", "frein", "pneu", "pneus", "carrosserie"],
        "category_aliases": ["automobile", "vehicule", "mecanique", "transport"],
        "negative_context": ["cosmetique", "beaute", "toilette"],
    },
    {
        "code_sh": "2523",
        "libelle": "Ciments hydrauliques, même colorés",
        "keywords": ["ciment", "ciments", "cement", "beton", "construction"],
        "category_aliases": ["construction", "batiment", "materiaux"],
    },
    {
        "code_sh": "7214",
        "libelle": "Barres et tiges en fer ou en acier",
        "keywords": ["acier", "fer", "barre", "barres", "metal", "metallique"],
        "category_aliases": ["construction", "batiment", "materiaux", "metallurgie"],
    },
    {
        "code_sh": "2505",
        "libelle": "Sables naturels de toute espèce",
        "keywords": ["sable", "sables", "sableux", "granulat"],
        "category_aliases": ["construction", "btp", "materiaux", "chantier"],
    },
    {
        "code_sh": "2517",
        "libelle": "Cailloux, graviers et pierres concassées",
        "keywords": ["gravier", "graviers", "caillou", "cailloux", "pierre", "pierres", "concasse"],
        "category_aliases": ["construction", "btp", "materiaux", "chantier"],
    },
    {
        "code_sh": "6904",
        "libelle": "Briques, hourdis, carreaux et pièces similaires en céramique",
        "keywords": ["brique", "briques", "parpaing", "parpaings", "hourdis", "bloc", "blocs"],
        "category_aliases": ["construction", "btp", "materiaux", "maconnerie"],
    },
    {
        "code_sh": "6907",
        "libelle": "Carreaux, dalles et pièces en céramique pour revêtements",
        "keywords": ["carrelage", "carreaux", "dalle", "dalles", "faience", "gres", "revetement"],
        "category_aliases": ["construction", "btp", "materiaux", "finition"],
    },
    {
        "code_sh": "7007",
        "libelle": "Verre de sécurité, trempé ou feuilleté",
        "keywords": ["vitre", "vitres", "verre", "verres", "vitrage", "pare-brise", "securite"],
        "category_aliases": ["construction", "btp", "materiaux", "menuiserie"],
    },
    {
        "code_sh": "7318",
        "libelle": "Vis, boulons, écrous et articles similaires en fer ou en acier",
        "keywords": ["vis", "visserie", "boulon", "boulons", "ecrou", "ecrous", "rondelle", "fixation"],
        "category_aliases": ["construction", "btp", "quincaillerie", "outillage"],
    },
    {
        "code_sh": "8205",
        "libelle": "Outils à main et outillage non dénommés ailleurs",
        "keywords": ["outil", "outils", "outillage", "marteau", "tournevis", "cle", "cles", "pince", "pinces", "niveau", "truelle", "machette"],
        "category_aliases": ["outillage", "btp", "construction", "bricolage"],
    },
    {
        "code_sh": "8207",
        "libelle": "Outils interchangeables pour outillage à main ou machines",
        "keywords": ["foret", "forets", "meche", "meches", "lame", "lames", "embout", "embouts", "fraise", "fraises"],
        "category_aliases": ["outillage", "btp", "construction", "mecanique"],
    },
    {
        "code_sh": "8467",
        "libelle": "Outils électromécaniques portatifs à moteur incorporé",
        "keywords": ["perceuse", "perceuses", "visseuse", "visseuses", "meuleuse", "meuleuses", "scie_electrique", "ponceuse", "marteau_piqueur"],
        "category_aliases": ["outillage", "btp", "construction", "electrique"],
    },
    {
        "code_sh": "8413",
        "libelle": "Pompes pour liquides et élévateurs de liquides",
        "keywords": ["pompe", "pompes", "surpresseur", "hydraulique", "irrigation"],
        "category_aliases": ["plomberie", "btp", "construction", "agriculture"],
    },
    {
        "code_sh": "8481",
        "libelle": "Articles de robinetterie et organes similaires",
        "keywords": ["robinet", "robinets", "vanne", "vannes", "robinetterie", "raccord", "raccords"],
        "category_aliases": ["plomberie", "btp", "construction", "sanitaire"],
    },
    {
        "code_sh": "8429",
        "libelle": "Bouteurs, niveleuses, excavateurs et engins de terrassement",
        "keywords": ["excavatrice", "excavatrices", "pelleteuse", "pelleteuses", "bulldozer", "tractopelle", "niveleuse", "engins"],
        "category_aliases": ["btp", "construction", "chantier", "travaux_publics"],
    },
    {
        "code_sh": "9406",
        "libelle": "Constructions préfabriquées",
        "keywords": ["prefabrique", "prefabriques", "bungalow", "modulaire", "modules", "base_vie"],
        "category_aliases": ["btp", "construction", "batiment", "chantier"],
    },
    {
        "code_sh": "3208",
        "libelle": "Peintures et vernis à base de polymères en milieu non aqueux",
        "keywords": ["peinture", "peintures", "vernis", "laque", "laques", "email", "enduit", "appret"],
        "category_aliases": ["btp", "construction", "finition", "decoration"],
    },
    {
        "code_sh": "4418",
        "libelle": "Ouvrages de menuiserie et pièces de charpente en bois",
        "keywords": ["bois", "menuiserie", "porte", "portes", "fenetre", "fenetres", "charpente_bois", "parquet"],
        "category_aliases": ["btp", "construction", "menuiserie", "batiment"],
    },
    {
        "code_sh": "3917",
        "libelle": "Tubes, tuyaux et accessoires en matières plastiques",
        "keywords": ["tuyau", "tuyaux", "tube", "tubes", "canalisation", "gaine", "pvc", "evacuation"],
        "category_aliases": ["plomberie", "btp", "construction", "sanitaire"],
    },
    {
        "code_sh": "7306",
        "libelle": "Tubes et tuyaux en fer ou en acier",
        "keywords": ["tube_acier", "tuyau_acier", "canalisation_acier", "profil", "profils"],
        "category_aliases": ["plomberie", "btp", "construction", "metallurgie"],
    },
    {
        "code_sh": "6910",
        "libelle": "Appareils sanitaires en céramique",
        "keywords": ["lavabo", "lavabos", "evier", "evier", "toilette", "wc", "baignoire", "douche", "sanitaire"],
        "category_aliases": ["plomberie", "btp", "construction", "salle_de_bain"],
    },
    {
        "code_sh": "8544",
        "libelle": "Fils, câbles et conducteurs électriques isolés",
        "keywords": ["cable", "cables", "fil_electrique", "fils", "conducteur", "electrique", "electricite"],
        "category_aliases": ["btp", "construction", "electricite", "electrique"],
    },
    {
        "code_sh": "8536",
        "libelle": "Appareillage électrique pour la protection ou la connexion des circuits",
        "keywords": ["interrupteur", "interrupteurs", "disjoncteur", "disjoncteurs", "prise", "prises", "tableau_electrique", "fusible"],
        "category_aliases": ["btp", "construction", "electricite", "electrique"],
    },
    {
        "code_sh": "6806",
        "libelle": "Matières minérales isolantes et matériaux calorifuges",
        "keywords": ["isolation", "isolant", "isolants", "laine_verre", "laine_roche", "polystyrene", "mousse", "calorifuge"],
        "category_aliases": ["btp", "construction", "materiaux", "etancheite"],
    },
    {
        "code_sh": "6905",
        "libelle": "Tuiles, éléments de cheminée et articles de construction en céramique",
        "keywords": ["tuile", "tuiles", "toiture", "toit", "couverture", "cheminee", "ardoise"],
        "category_aliases": ["btp", "construction", "toiture", "batiment"],
    },
    {
        "code_sh": "8426",
        "libelle": "Ponts roulants, grues et appareils de levage",
        "keywords": ["grue", "grues", "levage", "pont_roulant", "palan", "treuil", "manutention"],
        "category_aliases": ["btp", "construction", "chantier", "travaux_publics"],
    },
    {
        "code_sh": "8474",
        "libelle": "Machines pour le traitement des matières minérales et bétonnières",
        "keywords": ["betonniere", "betonnieres", "concasseur", "concasseurs", "criblage", "malaxeur", "broyeur"],
        "category_aliases": ["btp", "construction", "chantier", "travaux_publics"],
    },
    {
        "code_sh": "8427",
        "libelle": "Chariots de manutention et élévateurs",
        "keywords": ["chariot", "chariots", "elevateur", "elevateurs", "forklift", "transpalette", "manitou"],
        "category_aliases": ["btp", "construction", "chantier", "manutention"],
    },
    {
        "code_sh": "8428",
        "libelle": "Ascenseurs, monte-charges, convoyeurs et appareils de levage",
        "keywords": ["ascenseur", "ascenseurs", "monte_charge", "convoyeur", "convoyeurs", "escalator", "escalier_roulant"],
        "category_aliases": ["btp", "construction", "chantier", "manutention"],
    },
    {
        "code_sh": "2715",
        "libelle": "Mastics, enduits et mélanges bitumineux pour la construction",
        "keywords": ["bitume", "bitumes", "asphalte", "goudron", "enrobe", "etancheite"],
        "category_aliases": ["btp", "construction", "voirie", "routes"],
    },
    {
        "code_sh": "8430",
        "libelle": "Machines de terrassement, nivellement, excavation ou forage",
        "keywords": ["forage", "foreuse", "foreuses", "perforatrice", "perforatrices", "terrassement", "trancheuse", "tariere"],
        "category_aliases": ["btp", "construction", "chantier", "travaux_publics"],
    },
    {
        "code_sh": "8414",
        "libelle": "Pompes à air, compresseurs et ventilateurs",
        "keywords": ["compresseur", "compresseurs", "compresse", "ventilateur", "ventilateurs", "souffleur"],
        "category_aliases": ["btp", "construction", "industrie", "outillage"],
    },
    {
        "code_sh": "8502",
        "libelle": "Groupes électrogènes et convertisseurs rotatifs électriques",
        "keywords": ["groupe_electrogene", "electrogene", "generateur", "generateurs", "generator", "groupe_electrique"],
        "category_aliases": ["btp", "energie", "chantier", "electrique"],
    },
    {
        "code_sh": "6506",
        "libelle": "Casques et autres coiffures de protection",
        "keywords": ["casque", "casques", "casque_chantier", "protection_tete"],
        "category_aliases": ["btp", "securite", "chantier", "epi"],
    },
    {
        "code_sh": "6116",
        "libelle": "Gants de protection et gants en matières textiles",
        "keywords": ["gant", "gants", "gants_chantier", "gants_protection", "epi"],
        "category_aliases": ["btp", "securite", "chantier", "epi"],
    },
    {
        "code_sh": "3926",
        "libelle": "Autres articles de protection et ouvrages en matières plastiques",
        "keywords": ["gilet", "gilets", "gilet_reflechissant", "barriere", "barrieres", "protection_chantier"],
        "category_aliases": ["btp", "securite", "chantier", "epi"],
    },
    {
        "code_sh": "8424",
        "libelle": "Appareils à projeter, disperser ou pulvériser et extincteurs",
        "keywords": ["extincteur", "extincteurs", "incendie", "sprinkler", "pulverisateur", "projection"],
        "category_aliases": ["btp", "securite", "incendie", "chantier"],
    },
    {
        "code_sh": "9015",
        "libelle": "Instruments et appareils de géodésie, topographie et arpentage",
        "keywords": ["topographie", "topometre", "theodolite", "laser", "arpentage", "geometre", "gps_chantier"],
        "category_aliases": ["btp", "mesure", "chantier", "topographie"],
    },
    {
        "code_sh": "9026",
        "libelle": "Instruments de mesure ou de contrôle des liquides et des gaz",
        "keywords": ["manometre", "debitmetre", "thermometre", "mesure", "controle", "pression"],
        "category_aliases": ["btp", "mesure", "plomberie", "industrie"],
    },
    {
        "code_sh": "8468",
        "libelle": "Machines et appareils pour le brasage ou le soudage",
        "keywords": ["soudage", "soudeuse", "soudeuses", "poste_a_souder", "chalumeau", "brasage"],
        "category_aliases": ["btp", "outillage", "construction", "metallurgie"],
    },
    {
        "code_sh": "7309",
        "libelle": "Réservoirs, citernes et conteneurs en fer ou en acier",
        "keywords": ["reservoir", "reservoirs", "citerne", "citernes", "cuve", "cuves", "silo", "silos"],
        "category_aliases": ["btp", "construction", "industrie", "stockage"],
    },
    {
        "code_sh": "8425",
        "libelle": "Palans, treuils, cabestans et vérins",
        "keywords": ["palan", "palans", "treuil", "treuils", "verin", "verins", "cabestan"],
        "category_aliases": ["btp", "levage", "construction", "manutention"],
    },
    {
        "code_sh": "9102",
        "libelle": "Montres-bracelets, montres de poche et montres similaires",
        "keywords": ["montre", "montres", "watch", "watches", "bracelet", "horlogerie", "smartwatch"],
        "category_aliases": ["montre", "horlogerie", "accessoire", "bijou"],
    },
    {
        "code_sh": "8703",
        "libelle": "Voitures de tourisme et autres véhicules automobiles pour le transport de personnes",
        "keywords": ["vehicule", "vehicules", "voiture", "voitures", "automobile", "automobiles", "auto", "car", "cars"],
        "category_aliases": ["vehicule", "automobile", "auto", "transport"],
    },
    {
        "code_sh": "8704",
        "libelle": "Véhicules automobiles pour le transport de marchandises",
        "keywords": ["camion", "camions", "fourgon", "fourgons", "pickup", "utilitaire", "marchandises"],
        "category_aliases": ["vehicule", "transport", "utilitaire", "camion"],
    },
    {
        "code_sh": "8711",
        "libelle": "Motocycles, cycles à moteur et scooters",
        "keywords": ["deux_roues", "moto", "motocyclette", "scooter", "cyclomoteur", "mobylettes", "quad"],
        "category_aliases": ["moto", "motocycle", "scooter", "deux_roues", "transport"],
    },
    {
        "code_sh": "8712",
        "libelle": "Bicyclettes et autres cycles sans moteur",
        "keywords": ["deux_roues", "velo", "bicyclette", "cycle", "vtt", "tricycle"],
        "category_aliases": ["velo", "bicyclette", "cycle", "deux_roues", "sport"],
    },
    {
        "code_sh": "6109",
        "libelle": "T-shirts, chemises et autres vêtements de dessus",
        "keywords": ["tshirt", "tee", "shirt", "chemise", "vetement", "vêtement", "pull", "maille", "maillot", "polo", "tee-shirt", "haut", "veste"],
        "category_aliases": ["textile", "habillement", "vetement", "mode", "linge"],
    },
    {
        "code_sh": "5205",
        "libelle": "Toiles et tissus de coton",
        "keywords": ["tissu", "coton", "wax", "toile", "fibre", "fibre", "textile", "maille", "cotonnade"],
        "category_aliases": ["textile", "coton", "tissu", "fabric"],
    },
    {
        "code_sh": "9403",
        "libelle": "Autres meubles et ameublement",
        "keywords": ["meuble", "chaise", "table", "canape", "bureau", "ameublement", "fauteuil"],
        "category_aliases": ["mobilier", "ameublement", "interieur"],
    },
    {
        "code_sh": "3304",
        "libelle": "Produits cosmétiques et de toilette",
        "keywords": ["cosmetique", "savon", "huile", "beaute", "soin", "lait", "creme", "gel", "shampooing"],
        "category_aliases": ["beaute", "cosmetique", "soin", "toilette"],
        "negative_context": ["moteur", "moteur", "vehicule", "voiture", "automobile", "engine", "motor"],
    },
]

GLOBAL_HS_CODES_PATH = Path(__file__).resolve().parents[2] / "database" / "global_hs_codes.csv"


def load_global_hs_codes() -> list[dict[str, str]]:
    database_url = os.getenv("DATABASE_URL")
    if database_url and psycopg is not None:
        try:
            with psycopg.connect(database_url) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT hscode, description
                        FROM global_hs_codes
                        WHERE nomenclature_version = %s
                        ORDER BY hscode
                        """,
                        ("HS2022",),
                    )
                    rows = cursor.fetchall()
                    if rows:
                        return [
                            {
                                "code_sh": str(code),
                                "description_en": description,
                                "description_fr_a_completer": description,
                            }
                            for code, description in rows
                        ]
        except Exception:
            pass

    if not GLOBAL_HS_CODES_PATH.exists():
        return []

    with GLOBAL_HS_CODES_PATH.open("r", encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


GLOBAL_HS_CODES = load_global_hs_codes()


@dataclass
class MatchRequest:
    product_description: str
    category_hint: str | None = None


@dataclass
class MatchCandidate:
    code_sh: str
    libelle: str
    score: float
    reason: str


@dataclass
class MatchResponse:
    legal_note: str
    candidates: list[MatchCandidate] = field(default_factory=list[MatchCandidate])


def normalize_text(value: str) -> list[str]:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(character for character in text if not unicodedata.combining(character)).lower()
    for phrase, normalized_phrase in {
        "deux roues": "deux_roues",
        "huile moteur": "huile_moteur",
        "panneau solaire": "panneau_solaire",
        "eau minerale": "eau_minerale",
        "eau de toilette": "eau_toilette",
        "lave linge": "lave_linge",
        "piece automobile": "piece_automobile",
        "groupe electrogene": "groupe_electrogene",
        "poste a souder": "poste_a_souder",
        "aliment animaux": "aliment_animaux",
        "gants de chantier": "gants_chantier",
        "casque de chantier": "casque_chantier",
        "echafaudage metallique": "echafaudage_metallique",
    }.items():
        text = text.replace(phrase, normalized_phrase)
    text = re.sub(r"[^a-z0-9_\s]", " ", text)
    tokens = [token for token in text.split() if token]
    return [token for token in tokens if token not in NOISE_WORDS and len(token) > 1]


def clean_data_label(value: str | None) -> str:
    tokens = normalize_text(value or "")
    return " ".join(tokens) if tokens else ""


def score_candidates(description: str, category_hint: str | None = None) -> list[CandidateScore]:
    description_tokens = set(normalize_text(description))
    hint_tokens = set(normalize_text(category_hint or ""))
    scored: list[CandidateScore] = []

    for item in CANDIDATE_CODES:
        negative_context_hits = set(item.get("negative_context", [])) & description_tokens
        if negative_context_hits:
            continue

        keyword_hits = [token for token in description_tokens if token in item["keywords"]]
        for token in description_tokens:
            if token in keyword_hits or len(token) < 5:
                continue
            if any(SequenceMatcher(None, token, keyword).ratio() >= 0.90 for keyword in item["keywords"]):
                keyword_hits.append(token)
        hint_hits = [token for token in hint_tokens if token in item.get("category_aliases", [])]
        combined_hits: list[str] = []
        for token in keyword_hits + hint_hits:
            if token not in combined_hits:
                combined_hits.append(token)

        score = len(combined_hits)
        if score == 0:
            continue

        scored.append(
            {
                "code_sh": item["code_sh"],
                "libelle": item["libelle"],
                "score": float(score),
                "reason": f"Mots-clés trouvés : {', '.join(combined_hits)}",
            }
        )

    for item in GLOBAL_HS_CODES:
        searchable_text = " ".join(
            filter(
                None,
                [
                    clean_data_label(item.get("description_en")),
                    clean_data_label(item.get("description_fr_a_completer")),
                ],
            )
        )
        searchable_tokens = set(normalize_text(searchable_text))
        description_hits = [token for token in description_tokens if token in searchable_tokens]
        if not description_hits:
            continue

        scored.append(
            {
                "code_sh": item["code_sh"],
                "libelle": item.get("description_fr_a_completer") or item["description_en"],
                "score": len(description_hits),
                "reason": f"Nomenclature mondiale HS2022 : {', '.join(description_hits)}",
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    unique_codes: list[CandidateScore] = []
    for item in scored:
        if item["code_sh"] not in {candidate["code_sh"] for candidate in unique_codes}:
            unique_codes.append(item)
    return unique_codes[:3]


def match_product(payload: MatchRequest):
    description = (payload.product_description or "").strip()
    if not description:
        return MatchResponse(legal_note=LEGAL_NOTE, candidates=[])

    scored: list[CandidateScore] = score_candidates(description, payload.category_hint)

    if not scored:
        scored = [
            {
                "code_sh": "9999",
                "libelle": "Classification non déterminée — à valider par un commissionnaire agréé",
                "score": 0.0,
                "reason": "Aucune correspondance fiable détectée. Décris le produit plus précisément ou fais-le valider manuellement.",
            },
        ]

    candidates = [
        MatchCandidate(
            code_sh=item["code_sh"],
            libelle=item["libelle"],
            score=float(item["score"]),
            reason=item["reason"],
        )
        for item in scored[:3]
    ]

    return MatchResponse(legal_note=LEGAL_NOTE, candidates=candidates)

const noiseWords = new Set([
  'mot', 'mots', 'word', 'words', 'unknown', 'unknow', 'inconnu', 'inconnue', 'inconnus', 'inconnues',
  'objet', 'objets', 'article', 'articles', 'produit', 'produits', 'item', 'items', 'type', 'types',
  'generic', 'generique', 'generiques', 'specific', 'specifique', 'specifiques', 'particulier', 'particuliere',
  'particuliers', 'particulieres', 'autre', 'autres', 'divers', 'diverse', 'diverses'
]);

const catalog = [
  {
    code_sh: '8504',
    libelle: 'Chargeurs et adaptateurs électriques; transformateurs électriques',
    keywords: ['chargeur', 'adaptateur', 'transformateur', 'telephone', 'smartphone', 'usb', 'cable', 'portable']
  },
  {
    code_sh: '8711',
    libelle: 'Motocycles, cycles à moteur et scooters',
    keywords: ['deux_roues', 'moto', 'motocyclette', 'scooter', 'cyclomoteur', 'mobylettes', 'quad']
  },
  {
    code_sh: '1006',
    libelle: 'Riz',
    keywords: ['riz', 'rice']
  },
  {
    code_sh: '0901',
    libelle: 'Café, même torréfié ou décaféiné',
    keywords: ['cafe', 'coffee']
  },
  {
    code_sh: '3004',
    libelle: 'Médicaments présentés sous forme de doses ou conditionnés pour la vente au détail',
    keywords: ['medicament', 'medicaments', 'medicine', 'pharmacie', 'comprime', 'sirop']
  },
  {
    code_sh: '3303',
    libelle: 'Parfums, eaux de toilette et préparations de parfumerie',
    keywords: ['parfum', 'parfums', 'parfumerie', 'fragrance', 'toilette']
  },
  {
    code_sh: '2202',
    libelle: 'Boissons non alcooliques, eaux et autres boissons',
    keywords: ['boisson', 'boissons', 'drink', 'drinks', 'jus', 'soda', 'limonade', 'eau', 'eaux', 'rafraichissement']
  },
  {
    code_sh: '7606',
    libelle: 'Tôles et bandes en aluminium',
    keywords: ['aluminium', 'aluminum', 'allimunium', 'alu', 'metal', 'toles', 'bande']
  },
  {
    code_sh: '6403',
    libelle: 'Chaussures à semelles extérieures en caoutchouc, plastique, cuir ou matière textile',
    keywords: ['chaussure', 'chaussures', 'shoe', 'shoes', 'basket', 'sandale', 'sandales', 'botte', 'bottes']
  },
  {
    code_sh: '4202',
    libelle: 'Malles, valises, sacs et contenants similaires',
    keywords: ['sac', 'sacs', 'bag', 'bags', 'valise', 'valises', 'cartable', 'sacoche']
  },
  {
    code_sh: '8517',
    libelle: 'Téléphones, smartphones et appareils de communication',
    keywords: ['telephone', 'telephones', 'smartphone', 'smartphones', 'mobile', 'portable', 'iphone', 'android']
  },
  {
    code_sh: '8471',
    libelle: 'Machines automatiques de traitement de l’information et ordinateurs',
    keywords: ['ordinateur', 'ordinateurs', 'computer', 'computers', 'pc', 'laptop', 'clavier', 'souris']
  },
  {
    code_sh: '8418',
    libelle: 'Réfrigérateurs, congélateurs et autres appareils frigorifiques',
    keywords: ['refrigerateur', 'refrigerateurs', 'frigo', 'congelateur', 'congelateurs', 'freezer']
  },
  {
    code_sh: '8450',
    libelle: 'Machines à laver le linge',
    keywords: ['lave-linge', 'lavelinge', 'machine', 'laver', 'washing', 'washing-machine']
  },
  {
    code_sh: '8708',
    libelle: 'Parties et accessoires de véhicules automobiles',
    keywords: ['piece', 'pieces', 'auto', 'automobile', 'moteur', 'frein', 'pneu', 'pneus', 'carrosserie']
  },
  {
    code_sh: '2523',
    libelle: 'Ciments hydrauliques, même colorés',
    keywords: ['ciment', 'ciments', 'cement', 'beton', 'construction']
  },
  {
    code_sh: '7214',
    libelle: 'Barres et tiges en fer ou en acier',
    keywords: ['acier', 'fer', 'barre', 'barres', 'metal', 'metallique']
  },
  {
    code_sh: '2505',
    libelle: 'Sables naturels de toute espèce',
    keywords: ['sable', 'sables', 'granulat']
  },
  {
    code_sh: '2517',
    libelle: 'Cailloux, graviers et pierres concassées',
    keywords: ['gravier', 'graviers', 'caillou', 'cailloux', 'pierre', 'pierres', 'concasse']
  },
  {
    code_sh: '6904',
    libelle: 'Briques, hourdis, carreaux et pièces similaires en céramique',
    keywords: ['brique', 'briques', 'parpaing', 'parpaings', 'hourdis', 'bloc', 'blocs']
  },
  {
    code_sh: '6907',
    libelle: 'Carreaux, dalles et pièces en céramique pour revêtements',
    keywords: ['carrelage', 'carreaux', 'dalle', 'dalles', 'faience', 'gres', 'revetement']
  },
  {
    code_sh: '7318',
    libelle: 'Vis, boulons, écrous et articles similaires en fer ou en acier',
    keywords: ['vis', 'visserie', 'boulon', 'boulons', 'ecrou', 'ecrous', 'rondelle', 'fixation']
  },
  {
    code_sh: '8205',
    libelle: 'Outils à main et outillage non dénommés ailleurs',
    keywords: ['outil', 'outils', 'outillage', 'marteau', 'tournevis', 'cle', 'cles', 'pince', 'pinces', 'truelle']
  },
  {
    code_sh: '8207',
    libelle: 'Outils interchangeables pour outillage à main ou machines',
    keywords: ['foret', 'forets', 'meche', 'meches', 'lame', 'lames', 'embout', 'embouts', 'fraise', 'fraises']
  },
  {
    code_sh: '8467',
    libelle: 'Outils électromécaniques portatifs à moteur incorporé',
    keywords: ['perceuse', 'perceuses', 'visseuse', 'visseuses', 'meuleuse', 'meuleuses', 'ponceuse', 'marteau_piqueur']
  },
  {
    code_sh: '8413',
    libelle: 'Pompes pour liquides et élévateurs de liquides',
    keywords: ['pompe', 'pompes', 'surpresseur', 'hydraulique', 'irrigation']
  },
  {
    code_sh: '8481',
    libelle: 'Articles de robinetterie et organes similaires',
    keywords: ['robinet', 'robinets', 'vanne', 'vannes', 'robinetterie', 'raccord', 'raccords']
  },
  {
    code_sh: '8429',
    libelle: 'Bouteurs, niveleuses, excavateurs et engins de terrassement',
    keywords: ['excavatrice', 'excavatrices', 'pelleteuse', 'pelleteuses', 'bulldozer', 'tractopelle', 'niveleuse', 'engins']
  },
  {
    code_sh: '9406',
    libelle: 'Constructions préfabriquées',
    keywords: ['prefabrique', 'prefabriques', 'bungalow', 'modulaire', 'modules', 'base_vie']
  },
  {
    code_sh: '3208',
    libelle: 'Peintures et vernis à base de polymères',
    keywords: ['peinture', 'peintures', 'vernis', 'laque', 'laques', 'email', 'enduit', 'appret']
  },
  {
    code_sh: '4418',
    libelle: 'Ouvrages de menuiserie et pièces de charpente en bois',
    keywords: ['bois', 'menuiserie', 'porte', 'portes', 'fenetre', 'fenetres', 'charpente_bois', 'parquet']
  },
  {
    code_sh: '3917',
    libelle: 'Tubes, tuyaux et accessoires en matières plastiques',
    keywords: ['tuyau', 'tuyaux', 'tube', 'tubes', 'canalisation', 'gaine', 'pvc', 'evacuation']
  },
  {
    code_sh: '6910',
    libelle: 'Appareils sanitaires en céramique',
    keywords: ['lavabo', 'lavabos', 'evier', 'toilette', 'wc', 'baignoire', 'douche', 'sanitaire']
  },
  {
    code_sh: '8544',
    libelle: 'Fils, câbles et conducteurs électriques isolés',
    keywords: ['cable', 'cables', 'fil_electrique', 'fils', 'conducteur', 'electrique', 'electricite']
  },
  {
    code_sh: '8536',
    libelle: 'Appareillage électrique de protection ou connexion',
    keywords: ['interrupteur', 'interrupteurs', 'disjoncteur', 'disjoncteurs', 'prise', 'prises', 'fusible']
  },
  {
    code_sh: '6806',
    libelle: 'Matières minérales isolantes et matériaux calorifuges',
    keywords: ['isolation', 'isolant', 'isolants', 'laine_verre', 'laine_roche', 'polystyrene', 'mousse']
  },
  {
    code_sh: '6905',
    libelle: 'Tuiles et articles de construction en céramique',
    keywords: ['tuile', 'tuiles', 'toiture', 'toit', 'couverture', 'cheminee', 'ardoise']
  },
  {
    code_sh: '8426',
    libelle: 'Ponts roulants, grues et appareils de levage',
    keywords: ['grue', 'grues', 'levage', 'pont_roulant', 'palan', 'treuil', 'manutention']
  },
  {
    code_sh: '8474',
    libelle: 'Machines pour matières minérales et bétonnières',
    keywords: ['betonniere', 'betonnieres', 'concasseur', 'concasseurs', 'criblage', 'malaxeur', 'broyeur']
  },
  {
    code_sh: '8427',
    libelle: 'Chariots de manutention et élévateurs',
    keywords: ['chariot', 'chariots', 'elevateur', 'elevateurs', 'forklift', 'transpalette', 'manitou']
  },
  {
    code_sh: '8428',
    libelle: 'Ascenseurs, monte-charges, convoyeurs et appareils de levage',
    keywords: ['ascenseur', 'ascenseurs', 'monte_charge', 'convoyeur', 'convoyeurs', 'escalator', 'escalier_roulant']
  },
  {
    code_sh: '2715',
    libelle: 'Mastics, enduits et mélanges bitumineux pour la construction',
    keywords: ['bitume', 'bitumes', 'asphalte', 'goudron', 'enrobe', 'etancheite']
  },
  {
    code_sh: '8430',
    libelle: 'Machines de terrassement, nivellement, excavation ou forage',
    keywords: ['forage', 'foreuse', 'foreuses', 'perforatrice', 'perforatrices', 'terrassement', 'trancheuse', 'tariere']
  },
  {
    code_sh: '8414',
    libelle: 'Pompes à air, compresseurs et ventilateurs',
    keywords: ['compresseur', 'compresseurs', 'compresse', 'ventilateur', 'ventilateurs', 'souffleur']
  },
  {
    code_sh: '8502',
    libelle: 'Groupes électrogènes et convertisseurs rotatifs électriques',
    keywords: ['groupe_electrogene', 'electrogene', 'generateur', 'generateurs', 'generator', 'groupe_electrique']
  },
  {
    code_sh: '6506',
    libelle: 'Casques et autres coiffures de protection',
    keywords: ['casque', 'casques', 'casque_chantier', 'protection_tete']
  },
  {
    code_sh: '6116',
    libelle: 'Gants de protection et gants en matières textiles',
    keywords: ['gant', 'gants', 'gants_chantier', 'gants_protection', 'epi']
  },
  {
    code_sh: '3926',
    libelle: 'Autres articles de protection et ouvrages en matières plastiques',
    keywords: ['gilet', 'gilets', 'gilet_reflechissant', 'barriere', 'barrieres', 'protection_chantier']
  },
  {
    code_sh: '8424',
    libelle: 'Appareils à projeter, disperser ou pulvériser et extincteurs',
    keywords: ['extincteur', 'extincteurs', 'incendie', 'sprinkler', 'pulverisateur']
  },
  {
    code_sh: '9015',
    libelle: 'Instruments et appareils de géodésie, topographie et arpentage',
    keywords: ['topographie', 'topometre', 'theodolite', 'laser', 'arpentage', 'geometre', 'gps_chantier']
  },
  {
    code_sh: '9026',
    libelle: 'Instruments de mesure ou de contrôle des liquides et des gaz',
    keywords: ['manometre', 'debitmetre', 'thermometre', 'mesure', 'controle', 'pression']
  },
  {
    code_sh: '8468',
    libelle: 'Machines et appareils pour le brasage ou le soudage',
    keywords: ['soudage', 'soudeuse', 'soudeuses', 'poste_a_souder', 'chalumeau', 'brasage']
  },
  {
    code_sh: '7309',
    libelle: 'Réservoirs, citernes et conteneurs en fer ou en acier',
    keywords: ['reservoir', 'reservoirs', 'citerne', 'citernes', 'cuve', 'cuves', 'silo', 'silos']
  },
  {
    code_sh: '8425',
    libelle: 'Palans, treuils, cabestans et vérins',
    keywords: ['palan', 'palans', 'treuil', 'treuils', 'verin', 'verins', 'cabestan']
  },
  {
    code_sh: '9102',
    libelle: 'Montres-bracelets, montres de poche et montres similaires',
    keywords: ['montre', 'montres', 'watch', 'watches', 'horlogerie', 'smartwatch']
  },
  {
    code_sh: '8703',
    libelle: 'Voitures de tourisme et autres véhicules automobiles pour le transport de personnes',
    keywords: ['vehicule', 'vehicules', 'voiture', 'voitures', 'automobile', 'automobiles', 'auto', 'car', 'cars']
  },
  {
    code_sh: '8704',
    libelle: 'Véhicules automobiles pour le transport de marchandises',
    keywords: ['camion', 'camions', 'fourgon', 'fourgons', 'pickup', 'utilitaire', 'marchandises']
  },
  {
    code_sh: '8712',
    libelle: 'Bicyclettes et autres cycles sans moteur',
    keywords: ['deux_roues', 'velo', 'bicyclette', 'cycle', 'vtt', 'tricycle']
  },
  {
    code_sh: '6109',
    libelle: 'T-shirts, chemises et autres vêtements de dessus',
    keywords: ['tshirt', 'tee', 'shirt', 'chemise', 'vetement', 'vêtement', 'pull', 'maille', 'maillot', 'polo', 'haut']
  },
  {
    code_sh: '5205',
    libelle: 'Toiles et tissus de coton',
    keywords: ['tissu', 'coton', 'wax', 'toile', 'fibre', 'textile', 'maille', 'cotonnade']
  },
  {
    code_sh: '9403',
    libelle: 'Autres meubles et ameublement',
    keywords: ['meuble', 'chaise', 'table', 'canape', 'bureau', 'ameublement', 'fauteuil']
  },
  {
    code_sh: '1209',
    libelle: 'Graines, fruits et spores à ensemencer',
    keywords: ['semence', 'semences', 'graine', 'graines', 'seed', 'plantation']
  },
  {
    code_sh: '3105',
    libelle: 'Engrais minéraux ou chimiques',
    keywords: ['engrais', 'fertilisant', 'fertilisants', 'uree', 'azote', 'phosphate', 'potasse', 'nkp']
  },
  {
    code_sh: '3808',
    libelle: 'Insecticides, herbicides, fongicides et produits phytosanitaires',
    keywords: ['pesticide', 'pesticides', 'herbicide', 'herbicides', 'fongicide', 'insecticide', 'phytosanitaire']
  },
  {
    code_sh: '8432',
    libelle: 'Machines et appareils agricoles pour le travail du sol',
    keywords: ['charrue', 'charrues', 'semoir', 'semoirs', 'labour', 'cultivateur', 'moissonneuse', 'agricole']
  },
  {
    code_sh: '8701',
    libelle: 'Tracteurs agricoles et autres tracteurs',
    keywords: ['tracteur', 'tracteurs', 'tractor', 'motoculteur', 'motoculteurs']
  },
  {
    code_sh: '2309',
    libelle: 'Préparations pour l alimentation des animaux',
    keywords: ['aliment_animaux', 'nourriture_animaux', 'provende', 'aliment_betail', 'croquettes', 'fourrage']
  },
  {
    code_sh: '0207',
    libelle: 'Viandes et abats comestibles de volailles',
    keywords: ['poulet', 'poulets', 'volaille', 'volailles', 'viande', 'viandes', 'abats']
  },
  {
    code_sh: '0401',
    libelle: 'Lait et crème de lait',
    keywords: ['lait', 'laits', 'creme_lait', 'produit_laitier', 'laitier']
  },
  {
    code_sh: '3304',
    libelle: 'Produits cosmétiques et de toilette',
    keywords: ['cosmetique', 'savon', 'huile', 'beaute', 'soin', 'lait', 'creme', 'gel', 'shampooing']
  },
  {
    code_sh: '3003',
    libelle: 'Médicaments non conditionnés pour la vente au détail',
    keywords: ['medicament_vrac', 'substance_pharmaceutique', 'principe_actif', 'pharmaceutique']
  },
  {
    code_sh: '3005',
    libelle: 'Ouates, gazes, bandes et articles analogues à usage médical',
    keywords: ['pansement', 'pansements', 'compresse', 'compresses', 'gaze', 'bandage', 'sparadrap']
  },
  {
    code_sh: '8518',
    libelle: 'Microphones, haut-parleurs, écouteurs et appareils audio',
    keywords: ['microphone', 'micro', 'haut_parleur', 'enceinte', 'ecouteur', 'ecouteurs', 'casque_audio', 'audio']
  },
  {
    code_sh: '8523',
    libelle: 'Supports pour l enregistrement du son ou de données',
    keywords: ['disque_dur', 'ssd', 'cle_usb', 'carte_memoire', 'memoire', 'stockage', 'disque']
  },
  {
    code_sh: '8525',
    libelle: 'Appareils photographiques, caméras et appareils de prise de vues',
    keywords: ['camera', 'cameras', 'appareil_photo', 'photo', 'photos', 'video', 'videos', 'webcam', 'drone']
  },
  {
    code_sh: '8526',
    libelle: 'Appareils de radionavigation et radiotélécommande',
    keywords: ['gps', 'navigation', 'radar', 'geolocalisation', 'telecommande', 'drone_navigation']
  }
];

function normalizeText(value) {
  let text = String(value ?? '')
    .toLowerCase()
  ;['deux roues', 'huile moteur', 'panneau solaire', 'eau minerale', 'groupe electrogene', 'poste a souder', 'aliment animaux'].forEach((phrase) => {
    text = text.replace(phrase, phrase.replace(/ /g, '_'));
  });
  return text
    .replace(/[^a-z0-9_\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .filter((token) => !noiseWords.has(token));
}

function getMatchCandidates(description) {
  const tokens = new Set(normalizeText(description));
  const scored = catalog
    .map((item) => {
      const hits = item.keywords.filter((keyword) => tokens.has(keyword));
      return {
        code_sh: item.code_sh,
        libelle: item.libelle,
        score: hits.length,
        reason: hits.length ? `Mots-clés trouvés : ${hits.join(', ')}` : 'Aucun mot-clé fort détecté'
      };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  if (scored.length) {
    return scored;
  }

  return [
    {
      code_sh: '9999',
      libelle: 'Classification non déterminée — à valider par un commissionnaire agréé',
      score: 0,
      reason: 'Aucun mot-clé de correspondance détecté.'
    },
    {
      code_sh: '9999',
      libelle: 'Classification non déterminée — à valider par un commissionnaire agréé',
      score: 0,
      reason: 'Aucune correspondance fiable détectée.'
    }
  ];
}

function formatCurrency(value) {
  return `${new Intl.NumberFormat('fr-FR').format(Math.round(value))} CFA`;
}

function calculateCostFromState() {
  const cif = Number(document.getElementById('cifValue').value || 0);
  const freight = Number(document.getElementById('freightValue').value || 0);
  const insurance = Number(document.getElementById('insuranceValue').value || 0);
  const cifBase = cif + freight + insurance;
  const customsRate = Number(document.getElementById('customsRate').value || 0);
  const rsRate = Number(document.getElementById('rsRate').value || 0);
  const pcRate = Number(document.getElementById('pcRate').value || 0);
  const vatRate = Number(document.getElementById('vatRate').value || 0);
  const specificTaxes = Number(document.getElementById('specificTaxes').value || 0);

  const customs = cifBase * customsRate;
  const rs = cifBase * rsRate;
  const pc = cifBase * pcRate;
  const subtotalBeforeVat = cifBase + customs + rs + pc + cifBase * specificTaxes;
  const vat = subtotalBeforeVat * vatRate;
  const total = subtotalBeforeVat + vat;

  document.getElementById('customsValue').textContent = formatCurrency(customs);
  document.getElementById('rsValue').textContent = formatCurrency(rs);
  document.getElementById('pcValue').textContent = formatCurrency(pc);
  document.getElementById('vatValue').textContent = formatCurrency(vat);
  document.getElementById('totalValue').textContent = formatCurrency(total);
  return { customs, rs, pc, vat, total };
}

function renderMatchesFromApi() {
  const description = document.getElementById('productDescription').value || '';
  const list = document.getElementById('matchResults');
  list.innerHTML = '<li><span>Chargement…</span></li>';
  const apiBaseUrl = 'http://127.0.0.1:8000';

  fetch(`${apiBaseUrl}/match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_description: description })
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error('API unavailable');
      }
      const data = await response.json();
      const results = data.candidates && data.candidates.length ? data.candidates : getMatchCandidates(description);
      list.innerHTML = '';
      results.forEach((item) => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${item.code_sh} — ${item.libelle}</strong><span>${item.reason}</span>`;
        list.appendChild(li);
      });
    })
    .catch(() => {
      const fallbackResults = getMatchCandidates(description);
      list.innerHTML = '';
      fallbackResults.forEach((item) => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${item.code_sh} — ${item.libelle}</strong><span>${item.reason}</span>`;
        list.appendChild(li);
      });
    });
}

function calculateCost() {
  const apiBaseUrl = 'http://127.0.0.1:8000';

  fetch(`${apiBaseUrl}/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code_sh: '8504',
      product_label: document.getElementById('productDescription').value || 'Produit',
      cif_value: Number(document.getElementById('cifValue').value || 0),
      freight_value: Number(document.getElementById('freightValue').value || 0),
      insurance_value: Number(document.getElementById('insuranceValue').value || 0),
      customs_rate: Number(document.getElementById('customsRate').value || 0),
      rs_rate: Number(document.getElementById('rsRate').value || 0),
      pc_rate: Number(document.getElementById('pcRate').value || 0),
      vat_rate: Number(document.getElementById('vatRate').value || 0),
      specific_taxes: Number(document.getElementById('specificTaxes').value || 0),
    })
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error('API unavailable');
      }
      const data = await response.json();
      document.getElementById('customsValue').textContent = formatCurrency(data.breakdown.customs);
      document.getElementById('rsValue').textContent = formatCurrency(data.breakdown.rs);
      document.getElementById('pcValue').textContent = formatCurrency(data.breakdown.pc);
      document.getElementById('vatValue').textContent = formatCurrency(data.breakdown.vat);
      document.getElementById('totalValue').textContent = formatCurrency(data.total_cost);
    })
    .catch(() => {
      calculateCostFromState();
    });
}

function exportQuote() {
  const apiBaseUrl = 'http://127.0.0.1:8000';
  const payload = {
    code_sh: '8504',
    product_label: document.getElementById('productDescription').value || 'Produit',
    cif_value: Number(document.getElementById('cifValue').value || 0),
    freight_value: Number(document.getElementById('freightValue').value || 0),
    insurance_value: Number(document.getElementById('insuranceValue').value || 0),
    customs_rate: Number(document.getElementById('customsRate').value || 0),
    rs_rate: Number(document.getElementById('rsRate').value || 0),
    pc_rate: Number(document.getElementById('pcRate').value || 0),
    vat_rate: Number(document.getElementById('vatRate').value || 0),
    specific_taxes: Number(document.getElementById('specificTaxes').value || 0)
  };

  fetch(`${apiBaseUrl}/quote/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
    .then((response) => {
      if (!response.ok) throw new Error('Export unavailable');
      return response.blob();
    })
    .then((blob) => {
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'bleue-print-devis.html';
      link.click();
      URL.revokeObjectURL(url);
    });
}

function renderMatches() {
  renderMatchesFromApi();
}

document.getElementById('matchBtn').addEventListener('click', renderMatches);
document.getElementById('matchBtnSecondary').addEventListener('click', renderMatches);
document.getElementById('calculateBtn').addEventListener('click', calculateCost);
document.getElementById('exportBtn').addEventListener('click', exportQuote);

renderMatches();
calculateCost();

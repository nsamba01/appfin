# -*- coding: utf-8 -*-
"""Contenu intégral de l'OFFRE TECHNIQUE, structuré pour la mise en page.

Source unique du contenu : « OFFRE TECHNIQUE & MÉTHODOLOGIQUE UNICEF BURUNDI _
Consultant International Dr Gullit.pdf ».  Aucune section n'est supprimée, aucun
chiffre n'est modifié ; seules les coquilles manifestes ont été corrigées.
"""

TITLE = "OFFRE TECHNIQUE ET MÉTHODOLOGIQUE"
SUBTITLE = (
    "Appui à la mise en œuvre de la première phase du plan de passage à l’échelle "
    "de la Stratégie Nationale de Santé Communautaire (SNSC\u00a02025-2029) au Burundi"
)
CONSULTANT = "Consultant international : Dr Gullit Lufiauluisu, PhD"
REFERENCE = "Numéro de référence : TMC0007256"
DATE = "Novembre 2026"

TOC_SUBTITLE = "Offre technique et méthodologique"

# ---------------------------------------------------------------------------
# Le corps du document : liste de blocs.
#   ("h1",  numéro, titre)                 -> grande section
#   ("badge", texte)                       -> titre encadré (fond marron-gris, blanc)
#   ("sub", texte)                         -> intertitre capitales espacées
#   ("p", texte)                           -> paragraphe courant
#   ("ul", [items])                        -> liste à puces
#   ("ol", [items])                        -> liste numérotée
#   ("box", titre, [items])                -> encadré bordé
#   ("table", "risks"|"gantt")             -> tableau
#   ("note", texte)                        -> légende sous tableau
# ---------------------------------------------------------------------------

BODY = [
    ("h1", "01", "Résumé exécutif"),
    ("p", "La santé communautaire constitue l'un des piliers essentiels de la Couverture "
          "Sanitaire Universelle et de l'amélioration durable des indicateurs de santé "
          "maternelle, néonatale, infantile et adolescente. Le Gouvernement du Burundi a "
          "franchi une étape majeure avec la validation de la Stratégie Nationale de Santé "
          "Communautaire (SNSC 2025-2029), destinée à renforcer la prestation des services "
          "de santé communautaire et à accélérer l'accès équitable aux soins pour les "
          "populations les plus vulnérables."),
    ("p", "Afin d'assurer une mise en œuvre efficace de cette stratégie, l'UNICEF prévoit un "
          "accompagnement technique de haut niveau portant sur la mobilisation des "
          "ressources, le renforcement du leadership national, l'engagement des partenaires, "
          "l'organisation du Forum national de haut niveau sur la santé communautaire ainsi "
          "que le renforcement des capacités techniques des acteurs de mise en œuvre."),
    ("p", "Le Dr Gullit Lufiauluisu propose une approche intégrée combinant planification "
          "stratégique, mobilisation des ressources, accompagnement institutionnel, "
          "développement des capacités nationales et capitalisation des acquis. Cette "
          "approche vise à garantir non seulement la réalisation des livrables attendus mais "
          "également l'appropriation nationale des résultats et leur institutionnalisation "
          "durable."),
    ("lead", "L'intervention reposera sur quatre axes stratégiques :"),
    ("ul", [
        "Mobilisation des ressources et plaidoyer auprès des partenaires",
        "Préparation et accompagnement du Forum national de haut niveau",
        "Renforcement des capacités et appui technique à la mise en œuvre",
        "Consolidation des acquis et institutionnalisation des résultats",
    ]),
    ("p", "L'ensemble de la mission sera conduit selon les principes de gestion axée sur les "
          "résultats, de redevabilité, de participation multisectorielle et d'assurance "
          "qualité conformes aux standards des Nations Unies."),

    # ---------------------------------------------------------------- 02
    ("h1", "02", "Compréhension de la mission"),
    ("p", "La validation récente de la Stratégie Nationale de Santé Communautaire (SNSC) "
          "2025-2029 marque une étape déterminante dans les efforts du Gouvernement du "
          "Burundi visant à renforcer durablement les interventions communautaires et à "
          "accélérer les progrès vers la Couverture Sanitaire Universelle. Toutefois, la "
          "réussite de cette première phase de mise à l'échelle dépendra de la capacité des "
          "acteurs à mobiliser les ressources nécessaires, à coordonner efficacement les "
          "partenaires engagés et à renforcer les capacités des structures chargées de sa "
          "mise en œuvre."),
    ("p", "L'objectif général de cette mission est d'appuyer le Ministère de la Santé Publique "
          "dans l'opérationnalisation de cette stratégie à travers un accompagnement "
          "stratégique et technique favorisant la mobilisation des ressources, le "
          "renforcement du leadership national, l'engagement des partenaires et la "
          "consolidation des mécanismes de suivi et de redevabilité. Cette mission devra "
          "permettre de créer les conditions nécessaires pour assurer une mise en œuvre "
          "harmonisée, efficace et durable de la SNSC sur l'ensemble du territoire."),
    ("lead", "Cette mission intervient dans un contexte où :"),
    ("ul", [
        "La stratégie nationale a été récemment validée et nécessite désormais une mise en "
        "œuvre structurée et coordonnée",
        "Les besoins de financement de la phase initiale demeurent importants et exigent une "
        "stratégie de mobilisation des ressources adaptée",
        "La coordination des partenaires techniques et financiers nécessite un renforcement "
        "afin d'assurer une meilleure synergie des interventions",
        "Les capacités techniques des acteurs impliqués dans la mise en œuvre doivent être "
        "consolidées pour garantir la qualité et la pérennité des interventions",
        "Un mécanisme robuste de suivi des engagements et des résultats est indispensable "
        "pour assurer le succès du processus de passage à l'échelle",
    ]),
    ("p", "Dans cette perspective, le consultant international jouera un rôle de facilitateur "
          "stratégique et de conseiller technique auprès du Ministère de la Santé Publique, "
          "de l'UNICEF et des principales parties prenantes. Son appui visera à renforcer "
          "l'alignement des acteurs autour des priorités nationales tout en favorisant une "
          "mobilisation accrue des ressources et une meilleure gouvernance du processus de "
          "mise à l'échelle."),
    ("lead", "Plus spécifiquement, le consultant contribuera à :"),
    ("ul", [
        "Identifier les opportunités de financement et développer des arguments "
        "d'investissement en faveur de la SNSC",
        "Accroître l'alignement et l'engagement des partenaires autour des priorités "
        "nationales",
        "Soutenir le leadership du Ministère de la Santé Publique dans la coordination de la "
        "mise en œuvre de la stratégie",
        "Faciliter le dialogue politique de haut niveau à travers la préparation du Forum "
        "national sur la santé communautaire",
        "Renforcer les mécanismes de suivi, de coordination et de redevabilité liés à la mise "
        "en œuvre de la SNSC 2025-2029",
    ]),
    ("p", "Cette mission représente ainsi une opportunité stratégique pour consolider les "
          "acquis de la santé communautaire au Burundi, renforcer les partenariats "
          "institutionnels et mobiliser les investissements nécessaires à l'amélioration "
          "durable de la santé des populations."),

    # ---------------------------------------------------------------- 03
    ("h1", "03", "Objectifs de l'appui technique"),
    ("badge", "3.1. Objectif général"),
    ("p", "Contribuer à la réussite de la première phase du passage à l'échelle de la SNSC "
          "2025-2029 à travers un accompagnement stratégique, technique et institutionnel du "
          "Ministère de la Santé Publique du Burundi."),
    ("badge", "3.2. Objectifs spécifiques"),
    ("p", "Pour accompagner efficacement le Ministère de la Santé Publique dans la première "
          "phase de mise en œuvre de la Stratégie Nationale de Santé Communautaire (SNSC) "
          "2025-2029, la mission s'articulera autour d'objectifs spécifiques visant à "
          "renforcer simultanément le financement, la gouvernance, les capacités "
          "institutionnelles et les mécanismes de coordination nécessaires à une mise à "
          "l'échelle réussie des interventions de santé communautaire. L'approche proposée "
          "privilégiera le développement de solutions opérationnelles, l'alignement des "
          "partenaires autour des priorités nationales ainsi que l'institutionnalisation des "
          "acquis afin de garantir la durabilité des résultats au-delà de la période de "
          "consultation."),
    ("lead", "À cet effet, la mission poursuivra les objectifs spécifiques suivants :"),
    ("ul", [
        "Réaliser une analyse approfondie des besoins de financement de la SNSC, afin "
        "d'identifier les priorités d'investissement, les déficits de financement et les "
        "opportunités de mobilisation des ressources nécessaires à la mise en œuvre de la "
        "première phase du plan de passage à l'échelle.",
        "Soutenir la mobilisation des ressources nationales et internationales, à travers la "
        "cartographie des partenaires, le développement d'arguments d'investissement et le "
        "renforcement du dialogue avec les principaux bailleurs et partenaires de "
        "développement.",
        "Renforcer l'engagement des parties prenantes, en favorisant une meilleure "
        "coordination entre les acteurs gouvernementaux, les partenaires techniques et "
        "financiers, les organisations de la société civile et les autres institutions "
        "concernées par la mise en œuvre de la SNSC.",
        "Préparer et accompagner le Forum National de Haut Niveau sur la santé communautaire, "
        "comme plateforme stratégique de plaidoyer, de mobilisation des partenaires et de "
        "consolidation des engagements en faveur du passage à l'échelle des interventions "
        "communautaires.",
        "Renforcer les capacités des responsables techniques et des structures de mise en "
        "œuvre, à travers le coaching, le mentorat et le développement d'outils adaptés aux "
        "besoins opérationnels des programmes nationaux.",
        "Développer et améliorer les outils de pilotage, d'analyse et de suivi de la "
        "performance, afin de faciliter la prise de décision fondée sur les données "
        "probantes et d'améliorer le suivi de la mise en œuvre de la stratégie.",
        "Capitaliser et institutionnaliser les résultats de la mission, en documentant les "
        "bonnes pratiques, les leçons apprises et les recommandations stratégiques, tout en "
        "mettant en place des mécanismes permettant leur appropriation durable par les "
        "institutions nationales.",
    ]),
    ("p", "L'atteinte de ces objectifs contribuera à renforcer le leadership national, "
          "améliorer la coordination des partenaires et créer les conditions nécessaires à "
          "une mise en œuvre efficace, durable et financée de la SNSC 2025-2029 au Burundi."),

    # ---------------------------------------------------------------- 04
    ("h1", "04", "Approche méthodologique"),
    ("badge", "4.1. Principes directeurs"),
    ("p", "La réussite de la première phase de mise en œuvre de la Stratégie Nationale de "
          "Santé Communautaire (SNSC 2025-2029) repose sur une approche méthodologique "
          "participative, pragmatique et orientée vers les résultats. Conformément aux "
          "attentes de l'UNICEF et du Ministère de la Santé Publique, l'intervention "
          "proposée privilégiera le renforcement du leadership national, la mobilisation des "
          "acteurs clés, l'utilisation des données probantes et le transfert durable des "
          "compétences. Cette approche vise non seulement à produire les livrables attendus, "
          "mais également à créer les conditions favorables à une mise à l'échelle efficace, "
          "durable et financée des interventions de santé communautaire au Burundi."),
    ("lead", "L'approche proposée repose sur cinq principes fondamentaux :"),
    ("sub", "Appropriation nationale"),
    ("p", "Toutes les activités seront conduites sous le leadership du Ministère de la Santé "
          "Publique et en étroite collaboration avec les structures nationales concernées. "
          "Cette démarche favorisera l'appropriation des processus, des outils et des "
          "résultats par les institutions nationales afin de garantir la durabilité des "
          "acquis et leur intégration dans les mécanismes existants de gouvernance du "
          "secteur de la santé."),
    ("sub", "Participation multisectorielle"),
    ("p", "Compte tenu du caractère transversal de la santé communautaire, la mission "
          "impliquera activement l'ensemble des parties prenantes concernées, notamment les "
          "institutions gouvernementales, les partenaires techniques et financiers, les "
          "organisations de la société civile, les agences des Nations Unies ainsi que les "
          "structures de mise en œuvre. Cette approche collaborative permettra de renforcer "
          "l'alignement des interventions et de favoriser une vision commune des priorités "
          "de mise à l'échelle de la SNSC."),
    ("sub", "Utilisation de données probantes"),
    ("p", "Les analyses, recommandations et orientations stratégiques seront fondées sur des "
          "données fiables et vérifiables issues des documents stratégiques nationaux, des "
          "cadres programmatiques existants, des données de routine, des rapports de "
          "performance ainsi que des consultations réalisées avec les principales parties "
          "prenantes. Cette approche garantira la pertinence des recommandations proposées "
          "et leur adéquation avec les besoins réels du système de santé communautaire."),
    ("sub", "Gestion axée sur les résultats"),
    ("p", "L'ensemble des activités sera organisé selon une logique de gestion axée sur les "
          "résultats permettant de relier les actions menées aux produits attendus et aux "
          "effets recherchés. Une attention particulière sera accordée au respect des "
          "échéances, à la qualité des livrables, au suivi des engagements des acteurs et à "
          "la mesure des progrès réalisés dans le cadre de la mise en œuvre de la stratégie."),
    ("sub", "Renforcement durable des capacités"),
    ("p", "La mission sera conçue comme un processus d'apprentissage et de transfert de "
          "compétences au profit des équipes nationales. Les activités de coaching, "
          "d'accompagnement technique et de développement d'outils viseront à renforcer "
          "durablement les capacités des responsables techniques et des institutions "
          "impliquées afin qu'ils puissent poursuivre de manière autonome les efforts de "
          "mise en œuvre, de suivi et de mobilisation des ressources au-delà de la période "
          "de consultation."),
    ("p", "Ces principes directeurs constitueront le socle de l'ensemble de l'intervention et "
          "guideront les différentes étapes de la mission afin d'assurer une contribution "
          "tangible au renforcement du leadership national, à la mobilisation des ressources "
          "et à la réussite du passage à l'échelle de la SNSC 2025-2029 au Burundi."),

    ("badge", "4.2. Méthodologie par livrable"),
    ("p", "Afin de garantir l'atteinte des résultats attendus dans les délais impartis, la "
          "mission sera mise en œuvre selon une approche progressive articulée autour des "
          "quatre livrables définis dans les Termes de Référence. Chaque livrable fera "
          "l'objet d'un processus structuré associant analyse documentaire, consultations "
          "des parties prenantes, validation technique et accompagnement des structures "
          "nationales. Cette démarche permettra non seulement de produire des résultats de "
          "qualité répondant aux attentes de l'UNICEF et du Ministère de la Santé Publique, "
          "mais également de renforcer l'appropriation nationale des recommandations et des "
          "outils développés."),

    ("badge", "Livrable 1 — Analyse du financement et plan de mobilisation des ressources"),
    ("sub", "Étape 1 — Revue documentaire"),
    ("p", "Une analyse approfondie sera réalisée afin d'évaluer les priorités stratégiques, "
          "les besoins financiers et les engagements existants. Cette revue portera "
          "notamment sur :"),
    ("ul", [
        "La SNSC 2025-2029",
        "Les plans opérationnels",
        "Les cadres budgétaires existants",
        "Les rapports des partenaires",
        "Les engagements de financement en cours",
    ]),
    ("sub", "Étape 2 — Cartographie des partenaires"),
    ("p", "Des consultations ciblées seront organisées avec les acteurs clés afin de "
          "comprendre leurs priorités stratégiques, leurs contributions actuelles et leurs "
          "perspectives d'engagement dans la mise en œuvre de la SNSC. Les entretiens "
          "concerneront notamment :"),
    ("ul", [
        "Ministère de la Santé",
        "UNICEF",
        "OMS",
        "Banque mondiale",
        "Gavi",
        "Fonds mondial",
        "USAID",
        "ENABEL",
        "Union européenne et autres partenaires techniques et financiers",
    ]),
    ("sub", "Étape 3 — Analyse des écarts de financement"),
    ("p", "À partir des informations recueillies, une analyse détaillée des écarts de "
          "financement sera conduite afin d'identifier les domaines prioritaires nécessitant "
          "un investissement supplémentaire et les opportunités de mobilisation de nouvelles "
          "ressources."),
    ("lead", "Cette analyse permettra d'identifier :"),
    ("ul", [
        "Les besoins prioritaires",
        "Les déficits de financement",
        "Les opportunités de financement",
        "Les mécanismes innovants de mobilisation des ressources",
    ]),
    ("sub", "Étape 4 — Élaboration du Plan de Mobilisation des Ressources"),
    ("p", "Sur la base des résultats précédents, un plan de mobilisation des ressources sera "
          "élaboré afin d'orienter les efforts de plaidoyer et de coordination des "
          "partenaires autour des priorités nationales."),
    ("lead", "Ce document précisera :"),
    ("ul", [
        "Les investissements prioritaires",
        "Les partenaires ciblés",
        "Les messages clés de plaidoyer",
        "Les mécanismes de suivi",
    ]),
    ("box", "Produits attendus", [
        "Analyse du déficit de financement",
        "Cartographie des partenaires",
        "Rapport d'engagement interne UNICEF",
        "Plan de mobilisation des ressources",
    ]),

    ("badge", "Livrable 2 — Préparation du Forum National de Haut Niveau"),
    ("p", "Ce livrable vise à soutenir l'organisation du Forum National sur la santé "
          "communautaire qui constituera une plateforme stratégique de dialogue, de "
          "plaidoyer et de mobilisation des engagements des parties prenantes en faveur de "
          "la SNSC 2025-2029."),
    ("sub", "Analyse stratégique des parties prenantes"),
    ("p", "Une cartographie approfondie des acteurs permettra d'évaluer leur rôle potentiel "
          "dans le processus de mise à l'échelle de la santé communautaire."),
    ("lead", "L'analyse prendra en compte :"),
    ("ul", [
        "L'influence",
        "Le niveau d'engagement",
        "L'intérêt stratégique",
        "Le potentiel de contribution",
    ]),
    ("sub", "Préparation technique du forum"),
    ("p", "L'appui technique comprendra la préparation de l'ensemble des documents "
          "nécessaires à la réussite du forum et à la qualité des échanges stratégiques."),
    ("lead", "Les produits préparatoires comprendront notamment :"),
    ("ul", [
        "L'agenda détaillé",
        "Les messages clés",
        "Les notes de cadrage",
        "Les présentations techniques",
        "Les outils de facilitation",
    ]),
    ("sub", "Accompagnement de la tenue du Forum"),
    ("p", "Le consultant accompagnera les structures nationales et l'UNICEF dans la conduite "
          "du forum afin de faciliter l'atteinte des résultats attendus."),
    ("lead", "L'appui portera notamment sur :"),
    ("ul", [
        "La modération technique",
        "La documentation",
        "La consolidation des engagements",
    ]),
    ("box", "Produits attendus", [
        "Rapport préparatoire",
        "Documentation du forum",
        "Matrice des engagements",
        "Plan de suivi post-forum",
    ]),

    ("badge", "Livrable 3 — Renforcement des capacités et accompagnement technique"),
    ("p", "Cette composante vise à renforcer les capacités des structures nationales "
          "impliquées dans la mise en œuvre de la SNSC afin d'améliorer la qualité du "
          "pilotage, de l'analyse des données et du suivi de la performance."),
    ("sub", "Évaluation rapide des besoins"),
    ("p", "Une évaluation préliminaire sera réalisée afin d'identifier les forces, les "
          "lacunes et les besoins prioritaires des acteurs impliqués dans la mise en œuvre."),
    ("lead", "Cette phase portera sur :"),
    ("ul", [
        "L'analyse des capacités existantes",
        "L'identification des besoins en accompagnement technique",
        "L'évaluation des outils actuellement utilisés",
    ]),
    ("sub", "Développement des outils de renforcement des capacités"),
    ("p", "Des outils adaptés aux besoins des équipes techniques seront développés ou révisés "
          "afin de soutenir durablement la mise en œuvre de la SNSC."),
    ("lead", "Les outils à produire comprendront :"),
    ("ul", [
        "Des modules de coaching",
        "Des guides techniques",
        "Des supports de formation",
        "Des outils d'analyse des données",
    ]),
    ("sub", "Coaching des équipes"),
    ("p", "Un accompagnement pratique sera assuré au profit des responsables techniques afin "
          "de renforcer leurs capacités en matière de planification, de suivi et de "
          "coordination."),
    ("lead", "Cet accompagnement reposera sur :"),
    ("ul", [
        "Le mentorat",
        "Le coaching individualisé",
        "Les séances de partage d'expérience",
        "L'appui à la résolution des problèmes opérationnels",
    ]),
    ("sub", "Renforcement des outils de suivi"),
    ("p", "Les mécanismes de suivi seront consolidés afin d'améliorer la qualité de "
          "l'information et la prise de décision."),
    ("lead", "Les améliorations porteront notamment sur :"),
    ("ul", [
        "Les outils d'analyse",
        "Les mécanismes de reporting",
        "Les tableaux de bord",
    ]),
    ("box", "Produits attendus", [
        "Modules de formation",
        "Outil révisé d'analyse de données",
        "Cadre de coaching",
        "Documentation de l'appui technique fourni",
    ]),

    ("badge", "Livrable 4 — Institutionnalisation et capitalisation"),
    ("p", "Le dernier livrable vise à consolider les acquis de la mission, documenter les "
          "résultats obtenus et proposer des mécanismes permettant de pérenniser les actions "
          "engagées dans le cadre du passage à l'échelle de la SNSC."),
    ("sub", "Documentation des acquis"),
    ("p", "Une analyse rétrospective permettra de capitaliser les expériences acquises tout "
          "au long de la mission."),
    ("lead", "La documentation portera sur :"),
    ("ul", [
        "Les résultats atteints",
        "Les défis rencontrés",
        "Les leçons apprises",
    ]),
    ("sub", "Consolidation des recommandations"),
    ("p", "Les recommandations formulées seront revues avec les parties prenantes afin d'en "
          "assurer la pertinence et la faisabilité."),
    ("lead", "L'analyse prendra en compte :"),
    ("ul", [
        "La faisabilité",
        "La priorisation",
        "Les mécanismes de mise en œuvre",
    ]),
    ("sub", "Élaboration de la feuille de route de suivi"),
    ("p", "Une feuille de route opérationnelle sera élaborée afin de faciliter le suivi de la "
          "mise en œuvre des recommandations après la fin de la mission."),
    ("lead", "Cette feuille de route précisera :"),
    ("ul", [
        "Les responsabilités",
        "Les échéances",
        "Les indicateurs de suivi",
    ]),
    ("box", "Produits attendus", [
        "Notes techniques",
        "Rapports de suivi",
        "Matrice consolidée des recommandations",
        "Rapport final de consultation",
    ]),

    # ---------------------------------------------------------------- 05
    ("h1", "05", "Assurance qualité"),
    ("p", "La qualité des livrables constitue un élément central de la présente mission. "
          "Afin de garantir la pertinence, la fiabilité et l'utilité des produits développés "
          "pour le Ministère de la Santé Publique et l'UNICEF, un dispositif rigoureux "
          "d'assurance qualité sera mis en œuvre tout au long de la consultation. Ce "
          "dispositif visera à assurer la conformité des résultats aux attentes des Termes "
          "de Référence, tout en favorisant l'appropriation des recommandations par les "
          "principales parties prenantes."),
    ("lead", "L'assurance qualité s'appuiera notamment sur :"),
    ("ul", [
        "Des validations techniques régulières, permettant de vérifier l'adéquation des "
        "analyses et des orientations proposées avec les priorités nationales et les "
        "objectifs de la SNSC 2025-2029 ;",
        "Des consultations continues des parties prenantes, afin de garantir la prise en "
        "compte des besoins, attentes et contraintes des différents acteurs impliqués dans "
        "la mise en œuvre de la stratégie ;",
        "La triangulation des données et des sources d'information, à travers l'analyse "
        "croisée des documents stratégiques, des données programmatiques disponibles et des "
        "informations recueillies lors des entretiens et consultations ;",
        "Des mécanismes de revue par les pairs, permettant de renforcer la qualité technique "
        "des analyses, recommandations et outils développés dans le cadre de la mission ;",
        "Un contrôle qualité continu des livrables, afin de s'assurer du respect des "
        "standards techniques, de la cohérence des documents produits et de leur conformité "
        "aux exigences de l'UNICEF.",
    ]),
    ("p", "Par ailleurs, chaque livrable fera l'objet d'un processus de validation progressif "
          "garantissant l'amélioration continue des produits avant leur soumission "
          "définitive. Ce processus comprendra les étapes suivantes :"),
    ("ol", [
        "Une revue technique interne destinée à vérifier la qualité méthodologique, la "
        "cohérence des analyses et la conformité du livrable avec les objectifs assignés",
        "Une revue conjointe avec l'UNICEF et les parties prenantes concernées, permettant "
        "de recueillir les observations, recommandations et orientations complémentaires "
        "nécessaires",
        "L'intégration systématique des observations reçues, en vue d'améliorer la qualité, "
        "la pertinence et l'applicabilité des produits développés",
        "La soumission finale du livrable validé, accompagnée, le cas échéant, d'une "
        "présentation des principales conclusions et recommandations",
    ]),

    # ---------------------------------------------------------------- 06
    ("h1", "06", "Gestion des risques"),
    ("p", "La réussite de cette mission repose sur une anticipation adéquate des contraintes "
          "susceptibles d'affecter la qualité des livrables ou le respect des délais. Une "
          "approche proactive de gestion des risques sera ainsi mise en œuvre en étroite "
          "collaboration avec le Ministère de la Santé Publique et l'UNICEF afin d'identifier "
          "rapidement les difficultés potentielles et d'appliquer les mesures correctives "
          "appropriées."),
    ("lead", "Les principaux risques identifiés ainsi que les mesures d'atténuation "
             "proposées sont les suivants :"),
    ("table", "risks"),
    ("p", "Grâce à ce dispositif, les éventuels obstacles seront identifiés et traités "
          "rapidement afin de garantir la production de livrables de qualité, dans les "
          "délais convenus, et de contribuer efficacement à la mise en œuvre de la "
          "Stratégie Nationale de Santé Communautaire (SNSC 2025-2029)."),

    # ---------------------------------------------------------------- 07
    ("h1", "07", "Calendrier indicatif"),
    ("lead", "La programmation des activités de la mission s'établit comme suit :"),
    ("table", "gantt"),
    ("note", "Calendrier conforme à la durée de la mission prévue de 1,5 mois, soit "
             "6 semaines."),

    # ---------------------------------------------------------------- 08
    ("h1", "08", "Expertise du consultant international : le Dr Gullit Lufiauluisu"),
    ("p", "Le Dr Gullit Lufiauluisu est un expert international en santé publique disposant "
          "d'une solide expérience dans le renforcement des systèmes de santé, la santé "
          "communautaire, la planification stratégique, la mobilisation des ressources et "
          "l'accompagnement des réformes sanitaires dans plusieurs pays d'Afrique. Titulaire "
          "d'un Doctorat (PhD) en Santé Publique avec une spécialisation en gestion de la "
          "santé publique internationale de l'Université de la Renaissance d'Haïti, il est "
          "également détenteur d'un Master en Gestion des Projets de Santé et d'un Master en "
          "Transformation Sociale. Ce parcours académique multidisciplinaire lui a permis de "
          "développer une expertise reconnue en gouvernance sanitaire, planification "
          "stratégique, financement du secteur de la santé et développement des capacités "
          "institutionnelles."),
    ("p", "En sa qualité actuelle de Directeur Pays de ICHESS en République Démocratique du "
          "Congo, cabinet international spécialisé dans la recherche opérationnelle, le "
          "renforcement des systèmes de santé et la santé communautaire, il assure la "
          "direction technique de plusieurs initiatives régionales financées par l'UNICEF, "
          "le Fonds mondial, l'ONUSIDA, SANRU et d'autres partenaires de développement. "
          "Cette position lui permet de coordonner des équipes multidisciplinaires, "
          "d'assurer la qualité scientifique des interventions et de soutenir les "
          "gouvernements dans la formulation et la mise en œuvre de politiques de santé "
          "fondées sur les données probantes."),
    ("p", "Son expérience est particulièrement alignée sur les exigences du présent mandat, "
          "notamment dans le domaine de la santé communautaire. Il a joué un rôle clé dans "
          "l'évaluation du Plan Stratégique National de Santé Communautaire 2019-2022 de la "
          "RDC ainsi que dans l'élaboration du nouveau cycle 2025-2030 financé par "
          "l'UNICEF, un exercice impliquant l'analyse des performances, la consultation des "
          "parties prenantes, la définition des priorités stratégiques, l'estimation des "
          "besoins de financement et la formulation d'un cadre de mise en œuvre à grande "
          "échelle."),
    ("p", "Au-delà de la RDC, le Dr Gullit contribue actuellement, à travers les programmes "
          "régionaux d'ICHESS, à plusieurs initiatives de renforcement de la santé "
          "communautaire soutenues par le Fonds mondial dans le cadre du projet BIRCH. Ces "
          "interventions portent notamment sur l'évaluation des systèmes de santé "
          "communautaire, la cartographie des investissements, l'élaboration de politiques "
          "nationales de santé communautaire, le développement de plans stratégiques "
          "nationaux, l'élaboration de dossiers d'investissement et de plans de viabilité "
          "financière ainsi que l'évaluation de la maturité des systèmes de santé "
          "communautaires dans plusieurs pays d'Afrique, notamment la République du Congo, "
          "la Mauritanie, le Niger, le Tchad, Madagascar, la RCA et le Soudan du Sud."),
    ("lead", "Cette expérience régionale lui confère une expertise particulière dans les "
             "domaines explicitement recherchés par l'UNICEF pour cette mission :"),
    ("ul", [
        "L'élaboration et la mise en œuvre de stratégies nationales de santé "
        "communautaire ;",
        "La mobilisation des ressources et le développement de dossiers d'investissement ;",
        "L'analyse des déficits de financement et l'identification des opportunités de "
        "financement ;",
        "Le renforcement du leadership gouvernemental et de la coordination "
        "multisectorielle ;",
        "La planification stratégique et opérationnelle des systèmes de santé ;",
        "L'accompagnement du passage à l'échelle des interventions communautaires ;",
        "Le développement des capacités institutionnelles et le coaching des équipes "
        "nationales.",
    ]),
    ("p", "Le Dr Gullit possède également une expérience confirmée de collaboration avec les "
          "ministères de la Santé, l'UNICEF, l'OMS, le Fonds mondial et d'autres partenaires "
          "techniques et financiers. Il a notamment participé à l'élaboration du Plan "
          "National de Développement Sanitaire de Djibouti, à l'appui aux États Généraux de "
          "la Santé et à la réforme du système de santé de Djibouti, à "
          "l'opérationnalisation de la réforme de la gratuité des soins au Mali ainsi qu'à "
          "plusieurs exercices de chiffrage, de planification et de réforme des soins de "
          "santé primaires dans des contextes africains variés."),
    ("p", "Son expérience antérieure comme Coordonnateur National du Monitorage Amélioré "
          "pour l'Action (MAA) au Secrétariat Général à la Santé en RDC lui a permis de "
          "développer une expertise approfondie dans l'utilisation des données probantes "
          "pour l'amélioration des performances des systèmes de santé, l'identification des "
          "goulots d'étranglement et l'orientation des décisions stratégiques. Cette "
          "compétence est particulièrement pertinente pour accompagner le suivi des "
          "engagements, la mesure des progrès et l'institutionnalisation des résultats de la "
          "SNSC 2025-2029 au Burundi."),
    ("p", "Enfin, reconnu pour ses capacités de facilitation et de leadership, le Dr Gullit a "
          "conduit avec succès de nombreux ateliers nationaux et régionaux réunissant "
          "gouvernements, partenaires techniques et financiers, organisations de la société "
          "civile et agences internationales. Cette capacité à fédérer les acteurs autour "
          "d'une vision commune constitue un atout majeur pour la préparation du Forum "
          "National de Haut Niveau et pour le renforcement de l'engagement des parties "
          "prenantes dans la mise en œuvre de la Stratégie Nationale de Santé Communautaire "
          "du Burundi."),
    ("p", "La valeur ajoutée du Dr Gullit Lufiauluisu réside dans sa capacité à associer "
          "expertise technique, vision stratégique, mobilisation des ressources et "
          "accompagnement institutionnel afin de transformer les orientations de la SNSC "
          "2025-2029 en résultats concrets, durables et mesurables pour le système de santé "
          "communautaire burundais."),
]

# ---------------------------------------------------------------------------
# Données des tableaux (issues de l'offre technique, inchangées)
# ---------------------------------------------------------------------------
RISKS = [
    ("Disponibilité limitée des parties prenantes",
     "Planification précoce des consultations et validation anticipée du calendrier des "
     "rencontres avec les acteurs clés."),
    ("Retard dans l'accès aux données et documents stratégiques",
     "Coordination étroite avec le Ministère de la Santé Publique, l'UNICEF et les "
     "partenaires pour faciliter l'accès rapide aux informations requises."),
    ("Faible engagement institutionnel de certains acteurs",
     "Renforcement du plaidoyer et implication des décideurs dans les principales étapes du "
     "processus afin de favoriser l'adhésion et l'appropriation des résultats."),
    ("Contraintes logistiques ou organisationnelles",
     "Recours à des modalités flexibles de travail combinant réunions présentielles, "
     "virtuelles et hybrides pour assurer la continuité des activités."),
]

GANTT_ROWS = [
    ("Démarrage et revue documentaire", [1]),
    ("Analyse du financement et consultations", [1, 2]),
    ("Préparation du forum", [2, 3, 4]),
    ("Renforcement des capacités", [3, 4, 5]),
    ("Capitalisation et rapport final", [5, 6]),
]
GANTT_WEEKS = ["Semaine 1", "Semaine 2", "Semaine 3", "Semaine 4", "Semaine 5", "Semaine 6"]

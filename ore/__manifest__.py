{
    "name": "ORE",
    "category": "Uncategorized",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "application": True,
    "depends": ["mail", "web_timeline", "muk_branding"],
    "data": [
        "security/ir.model.access.csv",
        "security/ore.xml",
        "views/ore_ore.xml",
        "views/ore_arrondissement.xml",
        "views/ore_commentaire.xml",
        "views/ore_demande_adhesion.xml",
        "views/ore_demande_service.xml",
        "views/ore_echange_service.xml",
        "views/ore_membre.xml",
        "views/ore_occupation.xml",
        "views/ore_offre_service.xml",
        "views/ore_origine.xml",
        "views/ore_point_service.xml",
        "views/ore_provenance.xml",
        "views/ore_quartier.xml",
        "views/ore_region.xml",
        "views/ore_revenu_familial.xml",
        "views/ore_situation_maison.xml",
        "views/ore_type_communication.xml",
        "views/ore_type_service.xml",
        "views/ore_type_service_categorie.xml",
        "views/ore_type_service_sous_categorie.xml",
        "views/ore_type_telephone.xml",
        "views/ore_ville.xml",
        "views/ore_workflow.xml",
        "views/ore_workflow_relation.xml",
        "views/ore_workflow_state.xml",
        "views/res_config_settings_views.xml",
        "views/menu.xml",
        "data/ir_attachment.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "installable": True,
}

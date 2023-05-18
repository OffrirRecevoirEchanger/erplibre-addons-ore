{
    "name": "Demo ORE",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "depends": ["ore", "ore_data", "muk_branding"],
    "data": [
        "data/res_partner.xml",
        "data/res_company.xml",
        "data/user_demo.xml",
        "data/ore_offre_service.xml",
        "data/ore_demande_service.xml",
        "data/ore_echange_service.xml",
        "data/res_partner_favoris.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}

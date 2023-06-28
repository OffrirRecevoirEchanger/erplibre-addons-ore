# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Auth Signup Policy",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "depends": ["auth_signup", "website"],
    "data": [
        "templates/auth_signup_login_templates.xml",
        "views/assets.xml",
        "views/res_config_settings_views.xml",
        "views/website_page.xml",
    ],
    "application": False,
    "installable": True,
}

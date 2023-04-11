# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from pytz import timezone

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)
tz_montreal = timezone("America/Montreal")


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # All demo user is already accepted from list
        adhesion_ids = env["ore.demande.adhesion"].search([])
        for adhesion_id in adhesion_ids:
            adhesion_id.en_attente = False

        # TODO can move this in data
        env.ref("demo_ore.ore_membre_administrateur_mathieu_benoit").write(
            {
                "membre_favoris_ids": [
                    (
                        4,
                        env.ref("demo_ore.ore_membre_favoris_martin_petit").id,
                    ),
                    (
                        4,
                        env.ref(
                            "demo_ore.ore_membre_favoris_administrateur_mathieu_benoit"
                        ).id,
                    ),
                    (
                        4,
                        env.ref(
                            "demo_ore.ore_membre_favoris_alice_poitier"
                        ).id,
                    ),
                ]
            }
        )

        env.ref("demo_ore.ore_membre_denis_lemarchand").write(
            {
                "membre_favoris_ids": [
                    (
                        4,
                        env.ref("demo_ore.ore_membre_favoris_martin_petit").id,
                    ),
                    (
                        4,
                        env.ref(
                            "demo_ore.ore_membre_favoris_administrateur_mathieu_benoit"
                        ).id,
                    ),
                ]
            }
        )

        # General configuration
        values = {
            "ore_auto_accept_adhesion": True,
        }
        event_config = env["res.config.settings"].sudo().create(values)
        event_config.execute()

        for item in env["ir.actions.act_window"].search(
            [("name", "=", "ORE")]
        ):
            item.name = "Réseau"
        for item in env["ore.ore"].search([("nom", "=", "ORE de Laval")]):
            item.nom = "Municipalité de Sainte-Rose-Du-Nord"
        for item in env["ore.membre"].search([("nom", "=", "ORE Laval")]):
            item.nom = "Municipalité de Sainte-Rose-Du-Nord"

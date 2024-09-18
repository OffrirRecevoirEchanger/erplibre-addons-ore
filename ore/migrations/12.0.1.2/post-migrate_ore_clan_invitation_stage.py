import odoo
from odoo import SUPERUSER_ID, api
from odoo.tools import parse_version


def migrate(cr, version):
    if parse_version(version) == parse_version("12.0.1.1"):
        registry = odoo.registry(cr.dbname)
        env = api.Environment(cr, SUPERUSER_ID, {})
        default_ore_clan_invitation_stage_id = env[
            "ore.clan.invitation.stage"
        ].search([], order="sequence asc", limit=1)
        ore_clan_invitation_ids = env["ore.clan.invitation"].search(
            [("stage_id", "=", False)]
        )
        for invitation_id in ore_clan_invitation_ids:
            invitation_id.stage_id = default_ore_clan_invitation_stage_id.id

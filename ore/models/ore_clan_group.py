from odoo import _, api, fields, models


class OreClanGroup(models.Model):
    _name = "ore.clan.group"
    _description = "ore_clan_group"

    name = fields.Char()

    clan_id = fields.Many2one(
        comodel_name="ore.clan",
        string="Clan",
    )

    membre_create_id = fields.Many2one(
        comodel_name="ore.membre",
        string="Membre Create",
    )

    membre_list_ids = fields.Many2many(
        comodel_name="ore.membre",
        string="Membre List",
    )

    membre_responsable_ids = fields.Many2many(
        comodel_name="ore.membre",
        string="Membre Responsable",
    )

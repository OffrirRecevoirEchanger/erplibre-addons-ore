from odoo import _, api, fields, models


class OreClan(models.Model):
    _name = "ore.clan"
    _description = "ore_clan"

    name = fields.Char()

    autre_information = fields.Text()

    besoin_comble = fields.Text()

    organisation = fields.Char()

    ville_region = fields.Char()

    membre_admin_ids = fields.Many2many(
        comodel_name="ore.membre",
        relation="membre_admin_clan_rel",
        string="Membre Admin",
    )

    membre_create_id = fields.Many2one(
        comodel_name="ore.membre",
        string="Membre Create",
    )

    membre_list_ids = fields.Many2many(
        comodel_name="ore.membre",
        string="Membre",
        relation="membre_clan_participe_rel",
    )

    valeur_clan = fields.Text()

    membre_list_count = fields.Integer(
        string="Membre count",
        compute="_compute_membre_list_count",
        store=True,
    )

    @api.depends("membre_list_ids")
    def _compute_membre_list_count(self):
        for rec in self:
            rec.membre_list_count = len(rec.membre_list_ids)

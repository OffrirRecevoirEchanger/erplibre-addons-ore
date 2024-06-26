from odoo import _, api, fields, models


class OreClan(models.Model):
    _name = "ore.clan"
    _description = "ore_clan"

    name = fields.Char()

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, ce clan n'est plus en fonction,"
            " mais demeure accessible pour consultation historique."
        ),
    )

    # TODO not supported approuve
    approuve = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver ce clan.",
    )

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

    website_published = fields.Boolean(
        string="Clan rendu public",
        default=True,
        help="Le clan est publiée, sinon il est privée.",
    )

    @api.depends("membre_list_ids")
    def _compute_membre_list_count(self):
        for rec in self:
            rec.membre_list_count = len(rec.membre_list_ids)

    def website_publish_button(self):
        self.ensure_one()
        return self.write({"website_published": not self.website_published})

from datetime import datetime

from odoo import _, api, fields, models


class OREDemandeService(models.Model):
    _name = "ore.demande.service"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "ORE Demande Service"
    _rec_name = "titre"

    titre = fields.Char()

    active = fields.Boolean(
        string="Actif",
        default=True,
        track_visibility="onchange",
        help=(
            "Lorsque non actif, cet demande de services n'est plus en"
            " fonction, mais demeure accessible."
        ),
    )

    commentaire = fields.One2many(
        comodel_name="ore.commentaire",
        inverse_name="demande_service_id",
        help="Commentaire relation",
    )

    date_debut = fields.Date(
        string="Date début",
        track_visibility="onchange",
    )

    date_fin = fields.Date(
        string="Date fin",
        track_visibility="onchange",
    )

    description = fields.Text(
        track_visibility="onchange",
    )

    membre = fields.Many2one(
        comodel_name="ore.membre",
        track_visibility="onchange",
    )

    membre_favoris_ids = fields.Many2many(comodel_name="ore.membre")

    type_service_id = fields.Many2one(
        comodel_name="ore.type.service",
        track_visibility="onchange",
        string="Type de services",
    )

    user_id = fields.Many2one(related="membre.user_id")

    website_published = fields.Boolean(
        string="Demande publié",
        help="La demande est publiée, sinon il est privée.",
        track_visibility="onchange",
        default=True,
    )

    @api.multi
    def write(self, vals):
        status = super().write(vals)
        # Detect user
        ore_member = self.env["res.users"].browse(self.write_uid.id).partner_id
        for rec in self:
            self.env["bus.bus"].sendone(
                # f'["{self._cr.dbname}","{self._name}",{rec.id}]',
                "ore.notification.favorite",
                {
                    "timestamp": str(datetime.now()),
                    "data": vals,
                    "field_id": rec.id,
                    "canal": (
                        f'["{self._cr.dbname}","{self._name}",{ore_member.id}]'
                    ),
                },
            )
        return status

    @api.multi
    def website_publish_button(self):
        self.ensure_one()
        return self.write({"website_published": not self.website_published})

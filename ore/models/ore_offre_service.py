from datetime import datetime

from odoo import _, api, fields, models


class OREOffreService(models.Model):
    _name = "ore.offre.service"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "ORE Offre Service"
    _rec_name = "titre"

    titre = fields.Char(
        help="Résumé de l'offre, mise en valeur de la description.",
        track_visibility="onchange",
    )

    accompli = fields.Boolean(
        string="Accomplie",
        help="Cette offre de service est réalisée.",
        track_visibility="onchange",
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cet offre de services n'est plus en fonction,"
            " mais demeure accessible."
        ),
        track_visibility="onchange",
    )

    approuve = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver ce type de services.",
        track_visibility="onchange",
    )

    condition = fields.Html(
        string="Conditions",
        help="Conditions inhérentes à l'offre",
        track_visibility="onchange",
    )

    condition_autre = fields.Char(
        string="Condition autres",
        help="Autres conditions à informer",
        track_visibility="onchange",
    )

    date_affichage = fields.Date(
        string="Date d'affichage",
        track_visibility="onchange",
    )

    date_debut = fields.Date(
        string="Date de début",
        help="Date à partir de laquelle l'offre est valide.",
        track_visibility="onchange",
    )

    date_fin = fields.Date(
        string="Date de fin",
        help="Date jusqu'à laquelle l'offre est valide.",
        track_visibility="onchange",
    )

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
        track_visibility="onchange",
    )

    description = fields.Html(
        track_visibility="onchange",
    )

    deplacement = fields.Html(
        track_visibility="onchange",
    )

    disponibilite = fields.Char(
        string="Disponibilité",
        track_visibility="onchange",
    )

    entente_tarifiaire = fields.Html(
        track_visibility="onchange",
    )

    membre = fields.Many2one(
        comodel_name="ore.membre",
        help="Membre qui offre le service",
        track_visibility="onchange",
    )

    membre_favoris_ids = fields.Many2many(
        comodel_name="ore.membre",
        string="Membre Favoris",
        track_visibility="onchange",
    )

    nb_consultation = fields.Integer(string="Nombre de consultations")

    nom_offre_special = fields.Char(
        string="Nom de l'offre spéciale",
        help="Nom ou brève description de l'offre spéciale",
        track_visibility="onchange",
    )

    offre_special = fields.Boolean(
        string="Offre spéciale",
        track_visibility="onchange",
    )

    quoi_apporter = fields.Html(
        track_visibility="onchange",
    )

    tarif = fields.Char(
        track_visibility="onchange",
    )

    type_service_id = fields.Many2one(
        comodel_name="ore.type.service",
        string="Type de services",
        track_visibility="onchange",
    )

    user_id = fields.Many2one(
        related="membre.user_id",
        track_visibility="onchange",
    )

    website_published = fields.Boolean(
        string="Offre publié",
        default=True,
        help="L'offre est publiée, sinon il est privée.",
        track_visibility="onchange",
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

    def website_publish_button(self):
        self.ensure_one()
        return self.write({"website_published": not self.website_published})

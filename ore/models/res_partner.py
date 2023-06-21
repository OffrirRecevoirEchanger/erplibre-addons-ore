from datetime import date, datetime

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    commentaire = fields.One2many(
        comodel_name="ore.commentaire",
        inverse_name="membre_source",
        string="Commentaire membre source",
        help="Commentaire membre source relation",
    )

    commentaire_ids = fields.One2many(
        comodel_name="ore.commentaire",
        inverse_name="membre_viser",
        string="Commentaire membre visé",
        help="Commentaire membre visé relation",
    )

    est_un_point_service = fields.Boolean(string="Est un point de service")

    # TODO compute si contient des échanges?
    est_un_membre_ore = fields.Boolean(string="Est un membre du réseau ORE")

    reseau_ore_id = fields.Many2one(
        "ore.membre",
        string="Réseau ORE",
        help="Relation d'un réseau ORE, les responsables du membre.",
        index=True,
    )

    ore_membre_id = fields.Many2one(
        "ore.membre",
        string="Membre ore associé",
        help="Relation d'un membre du réseau ORE",
        index=True,
    )

    count_offre_service_ids = fields.Integer(
        related="ore_membre_id.count_offre_service_ids",
        readonly=True,
        help="Quantité des offres de service du membre",
    )

    count_demande_service_ids = fields.Integer(
        related="ore_membre_id.count_demande_service_ids",
        readonly=True,
        help="Quantité des demandes de service du membre",
    )

    count_echange_service_ids = fields.Integer(
        related="ore_membre_id.count_echange_service_ids",
        readonly=True,
        help="Quantité des échanges de service du membre",
    )

    bank_time = fields.Float(
        related="ore_membre_id.bank_time",
        string="Temps en banque",
        readonly=True,
        track_visibility="onchange",
    )

    bank_month_time = fields.Float(
        string="Temps en banque du présent mois",
        related="ore_membre_id.bank_month_time",
        readonly=True,
        track_visibility="onchange",
    )

    bank_max_service_offert = fields.Float(
        string="Temps maximal de service offert",
        related="ore_membre_id.bank_max_service_offert",
        readonly=True,
        track_visibility="onchange",
    )

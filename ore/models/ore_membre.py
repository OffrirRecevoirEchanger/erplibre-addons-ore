from datetime import date, datetime

from odoo import _, api, fields, models


class OREMembre(models.Model):
    _name = "ore.membre"
    _inherits = {"res.partner": "partner_id"}
    _description = "Information lié à un membre de ORE"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Membre",
        required=True,
        ondelete="cascade",
        track_visibility="onchange",
    )

    # achat_regrouper = fields.Boolean(
    #     string="Achat regroupé",
    #     track_visibility="onchange",
    # )

    # active = fields.Boolean(
    #     string="Actif",
    #     default=True,
    #     track_visibility="onchange",
    #     help=(
    #         "Lorsque non actif, ce membre n'est plus en fonction, mais demeure"
    #         " accessible."
    #     ),
    # )

    # adresse = fields.Char(
    #     track_visibility="onchange",
    # )

    annee_naissance = fields.Integer(
        string="Année de naissance",
        track_visibility="onchange",
    )

    age = fields.Integer(
        string="Âge",
        compute="_compute_age",
        track_visibility="onchange",
    )

    arrondissement = fields.Many2one(
        comodel_name="ore.arrondissement",
        track_visibility="onchange",
    )

    # bottin_courriel = fields.Boolean(
    #     string="Bottin courriel",
    #     track_visibility="onchange",
    # )

    # bottin_tel = fields.Boolean(
    #     string="Bottin téléphone",
    #     track_visibility="onchange",
    # )

    # codepostal = fields.Char(
    #     track_visibility="onchange",
    # )

    # commentaire = fields.One2many(
    #     comodel_name="ore.commentaire",
    #     inverse_name="membre_source",
    #     string="Commentaire membre source",
    #     help="Commentaire membre source relation",
    # )
    #
    # commentaire_ids = fields.One2many(
    #     comodel_name="ore.commentaire",
    #     inverse_name="membre_viser",
    #     string="Commentaire membre visé",
    #     help="Commentaire membre visé relation",
    # )

    # courriel = fields.Char(
    #     track_visibility="onchange",
    # )

    date_adhesion = fields.Date(
        string="Date de l'adhésion",
        track_visibility="onchange",
    )

    description_membre = fields.Boolean(
        string="Description du membre",
        track_visibility="onchange",
    )

    # est_un_point_service = fields.Boolean(string="Est un point de service")

    # # TODO compute si contient des échanges?
    # est_un_membre_ore = fields.Boolean(string="Est un membre du réseau ORE")

    # logo = fields.Binary(
    #     help="Logo du membre",
    #     track_visibility="onchange",
    # )

    image_attachment_id = fields.Many2one("ir.attachment")

    # membre_ca = fields.Boolean(
    #     string="Membre du CA",
    #     track_visibility="onchange",
    # )
    #
    # membre_conjoint = fields.Boolean(
    #     string="A un membre conjoint",
    #     track_visibility="onchange",
    # )

    # # TODO this is wrong, suppose to be many2many
    # membre_conjoint_id = fields.Integer(string="Membre conjoint")
    #
    # membre_principal = fields.Boolean(
    #     string="Membre principal",
    #     track_visibility="onchange",
    # )

    # reseau_ore_id = fields.Many2one(
    #     "ore.membre",
    #     string="Réseau ORE",
    #     help="Relation d'un réseau ORE, les responsables du membre.",
    #     index=True,
    # )

    # # TODO remove is_time_updated and force call _bank_time
    # is_time_updated = fields.Boolean(
    #     string="Time is updated",
    #     help="This variable is a trigger to update time.",
    # )

    # TODO remove
    # memo = fields.Text(string="Mémo")
    #
    # # TODO remove
    # nom_utilisateur = fields.Char(
    #     string="Nom du compte",
    #     track_visibility="onchange",
    # )

    occupation = fields.Many2one(
        comodel_name="ore.occupation",
        track_visibility="onchange",
    )

    origine = fields.Many2one(
        comodel_name="ore.origine",
        track_visibility="onchange",
    )

    offre_service_ids = fields.One2many(
        comodel_name="ore.offre.service",
        inverse_name="membre",
        string="Offre de service",
        help="Les offres de service du membre",
    )

    count_offre_service_ids = fields.Integer(
        compute="compute_count_offre_service_ids",
        store=True,
        help="Quantité des offres de service du membre",
    )

    demande_service_ids = fields.One2many(
        comodel_name="ore.demande.service",
        inverse_name="membre",
        string="Demande de service",
        help="Les demandes de service du membre",
    )

    count_demande_service_ids = fields.Integer(
        compute="compute_count_demande_service_ids",
        store=True,
        help="Quantité des demandes de service du membre",
    )

    echange_service_acheteur_ids = fields.One2many(
        comodel_name="ore.echange.service",
        inverse_name="membre_acheteur",
        string="Échange de service acheteur",
        help="Les échanges de service du membre acheteur",
    )

    echange_service_vendeur_ids = fields.One2many(
        comodel_name="ore.echange.service",
        inverse_name="membre_vendeur",
        string="Échange de service vendeur",
        help="Les échanges de service du membre vendeur",
    )

    count_echange_service_ids = fields.Integer(
        compute="compute_count_echange_service_ids",
        store=True,
        help="Quantité des échanges de service du membre",
    )

    membre_favoris_ids = fields.Many2many(
        string="Membre favoris",
        comodel_name="ore.membre.favoris",
        help="Liste des membres favoris",
    )

    # part_social_paye = fields.Boolean(
    #     string="Part social payé",
    #     track_visibility="onchange",
    # )

    # pas_communication = fields.Boolean(
    #     string="Pas de communication",
    #     track_visibility="onchange",
    # )

    interet = fields.Many2many(
        comodel_name="ore.membre.interet",
        help="Liste interet des membres",
    )

    langue_parle = fields.Many2many(
        string="Langue",
        comodel_name="ore.membre.langue_parle",
        help="Liste langues des membres",
    )

    # pret_actif = fields.Boolean(
    #     string="Prêt actif",
    #     track_visibility="onchange",
    # )

    profil_approuver = fields.Boolean(
        string="Profil approuvé",
        track_visibility="onchange",
    )

    provenance = fields.Many2one(
        comodel_name="ore.provenance",
        track_visibility="onchange",
    )

    quartier = fields.Many2one(
        comodel_name="ore.quartier",
        track_visibility="onchange",
    )

    # recevoir_courriel_groupe = fields.Boolean(
    #     string="Veut recevoir courriel de groupes",
    #     track_visibility="onchange",
    # )

    region = fields.Many2one(
        comodel_name="ore.region",
        string="Région",
        track_visibility="onchange",
    )

    revenu_familial = fields.Many2one(
        comodel_name="ore.revenu.familial",
        track_visibility="onchange",
        string="Revenu familial",
    )

    # sexe = fields.Selection(
    #     selection=[("femme", "Femme"), ("homme", "Homme"), ("autre", "Autre")],
    #     track_visibility="onchange",
    # )

    date_naissance = fields.Date(
        string="Date de naissance",
        track_visibility="onchange",
    )

    genre = fields.Selection(
        selection=[
            ("femme", "Femme"),
            ("homme", "Homme"),
            ("autre", "Autre"),
        ],
        track_visibility="onchange",
    )

    situation_maison = fields.Many2one(
        comodel_name="ore.situation.maison",
        string="Situation maison",
        track_visibility="onchange",
    )

    type_communication = fields.Many2one(
        comodel_name="ore.type.communication",
        string="Type de communications",
        track_visibility="onchange",
    )

    # user_id = fields.Many2one(
    #     comodel_name="res.users",
    #     string="User",
    #     track_visibility="onchange",
    # )

    ville = fields.Many2one(
        comodel_name="ore.ville",
        track_visibility="onchange",
    )

    antecedent_judiciaire_verifier = fields.Boolean(
        string="Antécédents judiciaires vérifiés",
        help="Vérifier par l'organisation",
        track_visibility="onchange",
    )

    introduction = fields.Char(
        help="Un petit texte qui décrit le membre.",
        track_visibility="onchange",
    )

    description = fields.Char(
        help="Un petit texte qui décrit le membre.",
        track_visibility="onchange",
    )

    motivation_membre = fields.Char(
        help="Pourquoi devenir un membre de réseau.",
        track_visibility="onchange",
    )

    bank_time = fields.Float(
        string="Temps en banque",
        compute="_bank_time",
        track_visibility="onchange",
        store=True,
    )

    bank_month_time = fields.Float(
        string="Temps en banque du présent mois",
        compute="_bank_time",
        track_visibility="onchange",
        store=True,
    )

    bank_max_service_offert = fields.Float(
        string="Temps maximal de service offert",
        compute="_bank_time",
        track_visibility="onchange",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        status = super().create(vals_list)
        for stat in status:
            stat.partner_id.ore_membre_id = stat.id
            ir_attach_id = self.env["ir.attachment"].create(
                {
                    "name": f"image_res_partner_{stat.id}",
                    "datas": stat.image,
                    "res_model": "ore.membre",
                    "res_id": stat.id,
                    "type": "url",
                }
            )
            stat.image_attachment_id = ir_attach_id.id
        return status

    @api.multi
    def write(self, vals):
        status = super().write(vals)

        # Detect user
        for rec in self:
            if "image" in vals.keys():
                # Update attachment with image
                image = vals.get("image")
                if rec.sudo().image_attachment_id:
                    rec.sudo().image_attachment_id.datas = image
                else:
                    ir_attach_id = self.env["ir.attachment"].create(
                        {
                            "name": f"image_res_partner_{rec.id}",
                            "datas": image,
                            "res_model": "ore.membre",
                            "res_id": rec.id,
                            "type": "url",
                        }
                    )
                    rec.sudo().image_attachment_id = ir_attach_id.id
            self.env["bus.bus"].sendone(
                # f'["{self._cr.dbname}","{self._name}",{rec.id}]',
                "ore.notification.favorite",
                {
                    "timestamp": str(datetime.now()),
                    "data": vals,
                    "field_id": rec.id,
                    "canal": f'["{self._cr.dbname}","{self._name}",{rec.id}]',
                },
            )
        return status

    @api.multi
    @api.depends("offre_service_ids")
    def compute_count_offre_service_ids(self):
        for rec in self:
            rec.count_offre_service_ids = len(rec.offre_service_ids)

    @api.multi
    @api.depends("demande_service_ids")
    def compute_count_demande_service_ids(self):
        for rec in self:
            rec.count_demande_service_ids = len(rec.demande_service_ids)

    @api.multi
    @api.depends("echange_service_acheteur_ids", "echange_service_vendeur_ids")
    def compute_count_echange_service_ids(self):
        for rec in self:
            rec.count_echange_service_ids = len(
                rec.echange_service_acheteur_ids
            ) + len(rec.echange_service_vendeur_ids)

    @api.depends(
        "echange_service_acheteur_ids",
        "echange_service_vendeur_ids",
        # "is_time_updated",
    )
    def _bank_time(self):
        # TODO wrong dependency
        # TODO use recompute instead of is_time_updated to force recompute
        # TODO calculate transaction difference
        for rec in self:
            this_month = datetime.now().month
            this_year = datetime.now().year
            bank_time = sum(
                [
                    a.nb_heure + a.nb_heure_duree_trajet
                    for a in rec.echange_service_vendeur_ids
                    if a.transaction_valide
                ]
            ) - sum(
                [
                    a.nb_heure + a.nb_heure_duree_trajet
                    for a in rec.echange_service_acheteur_ids
                    if a.transaction_valide
                ]
            )
            bank_max_service_offert = sum(
                [
                    a.nb_heure + a.nb_heure_duree_trajet
                    for a in rec.echange_service_vendeur_ids
                    if a.transaction_valide
                ]
            )
            bank_time_month = sum(
                [
                    a.nb_heure + a.nb_heure_duree_trajet
                    for a in rec.echange_service_vendeur_ids
                    if a.transaction_valide
                    and a.date_echange
                    and a.date_echange.month == this_month
                    and a.date_echange.year == this_year
                ]
            ) - sum(
                [
                    a.nb_heure + a.nb_heure_duree_trajet
                    for a in rec.echange_service_acheteur_ids
                    if a.transaction_valide
                    and a.date_echange
                    and a.date_echange.month == this_month
                    and a.date_echange.year == this_year
                ]
            )

            rec.bank_time = bank_time
            rec.bank_month_time = bank_time_month
            rec.bank_max_service_offert = bank_max_service_offert

    @api.depends("annee_naissance")
    def _compute_age(self):
        for rec in self:
            if not rec.annee_naissance:
                rec.age = 0
            else:
                today = date.today()
                # TODO algorithme avec date de naisance et non année de naissance
                # rec.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                rec.age = today.year - rec.annee_naissance

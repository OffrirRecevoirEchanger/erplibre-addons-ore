from odoo import _, api, fields, models


class OREDemandeAdhesion(models.Model):
    _name = "ore.demande.adhesion"
    _description = "ORE Demande Adhesion"
    _rec_name = "nom_complet"

    nom_complet = fields.Char(
        string="Nom complet",
        compute="_compute_nom_complet",
        store=True,
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cet demande d'adhésion n'est plus en fonction,"
            " mais demeure accessible."
        ),
    )

    courriel = fields.Char()

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
    )

    en_attente = fields.Boolean(
        string="En attente",
        default=True,
    )

    nom = fields.Char()

    poste = fields.Char()

    prenom = fields.Char(string="Prénom")

    telephone = fields.Char(string="Téléphone")

    transferer = fields.Boolean(string="Transféré")

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )

    @api.depends("nom", "prenom")
    def _compute_nom_complet(self):
        for rec in self:
            if rec.nom and rec.prenom:
                rec.nom_complet = f"{rec.prenom} {rec.nom}"
            elif rec.nom:
                rec.nom_complet = f"{rec.nom}"
            elif rec.prenom:
                rec.nom_complet = f"{rec.prenom}"
            else:
                rec.nom_complet = False

    @api.model_create_multi
    def create(self, vals_list):
        vals = super(OREDemandeAdhesion, self).create(vals_list)
        # Automatic accept, create member
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ore.ore_auto_accept_adhesion")
        ):
            default_ore_society = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("ore.ore_default_societe")
            )
            ore_default_free_time = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("ore.ore_default_free_time", 0)
            )
            if not default_ore_society:
                raise Exception(
                    "Need to define ORE society, please contact the"
                    " administrator."
                )
            society_id = self.env["ore.membre"].browse(
                int(default_ore_society)
            )
            # TODO move this into ore, do refactoring (merge partner and member), add configuration
            lst_data = []
            for val in vals:
                data = {
                    "profil_approuver": True,
                    "name": val.nom,
                    "parent_id": self.env.ref("base.main_partner").id,
                    "reseau_ore_id": society_id.id,
                    "user_id": val.user_id.id,
                    "partner_id": val.user_id.partner_id.id,
                    "region": society_id.region.id,
                    "ville": society_id.ville.id,
                }
                lst_data.append(data)
            membre_ids = self.env["ore.membre"].create(lst_data)
            # Force add initial time
            lst_data = []
            for membre_id in membre_ids:
                data = {
                    "date_echange": fields.Datetime.now(),
                    "nb_heure": float(ore_default_free_time),
                    "type_echange": "offre_ponctuel",
                    "transaction_valide": True,
                    "membre_acheteur": society_id.id,
                    "membre_vendeur": membre_id.id,
                }
                lst_data.append(data)
            self.env["ore.echange.service"].create(lst_data)
        return vals

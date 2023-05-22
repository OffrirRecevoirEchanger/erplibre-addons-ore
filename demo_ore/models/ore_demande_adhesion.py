from odoo import _, api, fields, models


class OREDemandeAdhesion(models.Model):
    _inherit = "ore.demande.adhesion"
    _description = "ORE Demande Adhesion DEMO"

    @api.model_create_multi
    def create(self, vals_list):
        vals = super(OREDemandeAdhesion, self).create(vals_list)
        # Automatic accept, create member
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ore.ore_auto_accept_adhesion")
        ):
            # TODO move this into ore, do refactoring (merge partner and member), add configuration
            lst_data = []
            for val in vals:
                data = {
                    # "ore": val.ore.id,
                    "profil_approuver": True,
                    "nom": val.nom,
                    # "prenom": val.prenom,
                    "user_id": val.user_id.id,
                    "partner_id": val.user_id.partner_id.id,
                    "region": self.env.ref(
                        "ore_data.ore_region_saguenay_lac_saint_jean"
                    ).id,
                    "ville": self.env.ref(
                        "ore_data.ore_ville_sainte_rose_du_nord"
                    ).id,
                }
                lst_data.append(data)
            membre_ids = self.env["res.partner"].create(lst_data)
            # Force add initial time
            lst_data = []
            for membre_id in membre_ids:
                data = {
                    "date_echange": fields.Datetime.now(),
                    "nb_heure": 15,
                    "type_echange": "offre_ponctuel",
                    "transaction_valide": True,
                    "membre_acheteur": self.env.ref("base.main_partner").id,
                    "membre_vendeur": membre_id.id,
                }
                lst_data.append(data)
            self.env["ore.echange.service"].create(lst_data)
        return vals

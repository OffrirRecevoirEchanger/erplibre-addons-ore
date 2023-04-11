from odoo import _, api, fields, models


class OREWorkflow(models.Model):
    _name = "ore.workflow"
    _description = "ORE Workflow"

    name = fields.Char(string="Nom")

    diagram_relation_ids = fields.One2many(
        comodel_name="ore.workflow.relation",
        inverse_name="diagram_id",
        string="Relation",
    )

    diagram_state_ids = fields.One2many(
        comodel_name="ore.workflow.state",
        inverse_name="diagram_id",
        string="State",
    )

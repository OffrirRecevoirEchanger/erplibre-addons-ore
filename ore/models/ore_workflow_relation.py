from odoo import _, api, fields, models


class OREWorkflowRelation(models.Model):
    _name = "ore.workflow.relation"
    _description = "ORE Workflow Relation"

    name = fields.Char(string="Nom")

    active = fields.Boolean(
        string="Actif",
        default=True,
        help="Lorsque non actif, cette relation n'est plus visible.",
    )

    not_implemented = fields.Boolean(
        string="Pas implémenté",
        help="Fonctionnalité officiellement non supporté.",
    )

    body_html = fields.Html(string="HTML")

    diagram_id = fields.Many2one(
        comodel_name="ore.workflow",
        string="Diagram",
    )

    icon = fields.Char(string="icon")

    # TODO create a variable to detect if state_src contains a type selection_dynamique to enable is_dynamic
    is_dynamic = fields.Boolean(
        string="Is dynamic", help="Use for type selection_dynamique"
    )

    state_dst = fields.Many2one(
        comodel_name="ore.workflow.state",
        string="State destination",
    )

    state_src = fields.Many2one(
        comodel_name="ore.workflow.state",
        string="State source",
    )

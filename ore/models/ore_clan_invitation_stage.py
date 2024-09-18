# Copyright 2024 TechnoLibre inc. - Mathieu Benoit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, exceptions, fields, models, tools

_logger = logging.getLogger(__name__)


class OreClanInvitationStage(models.Model):
    _name = "ore.clan.invitation.stage"
    _description = "Stage for clan invitation"
    _order = "sequence, name, id"

    name = fields.Char()

    description = fields.Char()

    sequence = fields.Integer(
        default=10,
        help="Used to order new project stages. Lower is better.",
    )

    fold = fields.Boolean(
        string="Folded in Pipeline",
        help=(
            "This stage is folded in the kanban view when there are no records"
            " in that stage to display."
        ),
    )

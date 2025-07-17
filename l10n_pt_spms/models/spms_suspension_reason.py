# Copyright 2025 Dixmit
# Copyright 2025 NuoBiT - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SpmsSuspensionReason(models.Model):
    _name = "spms.suspension.reason"
    _description = "SPMS Suspension Reason"

    code = fields.Char(required=True)
    name = fields.Char(required=True)

    _sql_constraints = [
        ("uniq", "unique(code)", "The code must be unique"),
    ]

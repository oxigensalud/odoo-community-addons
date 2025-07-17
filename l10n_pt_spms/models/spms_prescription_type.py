# Copyright 2025 Dixmit
# Copyright 2025 NuoBiT - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SpmsPrescriptionType(models.Model):
    _name = "spms.prescription.type"
    _description = "SPMS Prescription Type"

    code = fields.Char(required=True)
    name = fields.Char(required=True)

    _sql_constraints = [
        ("uniq", "unique(code)", "The code must be unique"),
    ]

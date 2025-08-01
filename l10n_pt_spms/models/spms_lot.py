# Copyright 2025 Dixmit
# Copyright 2025 NuoBiT - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SpmsLot(models.Model):
    _name = "spms.lot"
    _description = "SPMS Lot"

    name = fields.Char(required=True)
    code = fields.Char(required=True)

    _sql_constraints = [
        ("uniq", "unique(name)", "The name of the lot must be unique."),
        ("uniq", "unique(code)", "The code of the lot must be unique."),
    ]

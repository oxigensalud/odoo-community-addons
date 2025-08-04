# Copyright 2025 NuoBiT - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_spms = fields.Boolean(
        string="Is SPMS",
        help="If checked, this partner is configured to work with SPMS.",
        default=False,
        required=True,
    )

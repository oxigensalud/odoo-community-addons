# Copyright 2025 Dixmit
# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    spms_information = fields.Boolean()
    spms_available = fields.Boolean(
        string="SPMS Available", compute="_compute_spms_available"
    )

    @api.depends_context("company")
    def _compute_spms_available(self):
        available = self.env.company._is_spms_company()
        for partner in self:
            partner.spms_available = available

# Copyright 2025 Dixmit
# Copyright 2025 NuoBiT - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    spms_lot_id = fields.Many2one(
        comodel_name="spms.lot",
        compute="_compute_spms_lot",
        inverse="_inverse_spms_lot",
        store=True,
    )

    @api.depends("product_variant_ids", "product_variant_ids.spms_lot_id")
    def _compute_spms_lot(self):
        templates_wo_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in templates_wo_variants:
            template.spms_lot_id = template.product_variant_ids.spms_lot_id
        for template in self - templates_wo_variants:
            template.spms_lot_id = False

    def _inverse_spms_lot(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.spms_lot_id = template.spms_lot_id

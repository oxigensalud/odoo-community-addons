# Copyright 2025 Dixmit
# Copyright 2025 NuoBiT - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    spms_lot_id = fields.Many2one(
        comodel_name="spms.lot",
    )

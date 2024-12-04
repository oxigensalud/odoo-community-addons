# Copyright 2023 Dixmit
# Copyright NuoBiT Solutions - Frank Cespedes <fcespedes@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    lot_id = fields.Many2one(
        "stock.production.lot", readonly=True, copy=False, tracking=True
    )
    supplier_lot_number = fields.Char(
        compute="_compute_supplier_number",
        inverse="_inverse_supplier_lot_number",
        readonly=False,
        store=True,
    )
    supplier_product_id = fields.Many2one(
        "product.product",
        compute="_compute_supplier_product",
        inverse="_inverse_supplier_lot_number",
        domain=[
            ("type", "=", "product"),
            ("tracking", "=", "serial"),
            ("maintenance_lot", "=", True),
        ],
        readonly=False,
        tracking=True,
    )
    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Reception",
        readonly=False,
        copy=False,
        domain=[("picking_type_id.code", "=", "incoming")],
        tracking=True,
    )
    stock_move_line_id = fields.Many2one("stock.move.line", readonly=True, copy=False)
    purchase_id = fields.Many2one(
        comodel_name="purchase.order",
        compute="_compute_purchase",
        readonly=True,
        store=True,
        copy=False,
    )
    product_brand_id = fields.Many2one(
        "product.brand", related="supplier_product_id.product_brand_id"
    )
    stock_location_id = fields.Many2one("stock.location", string="Stock Location")

    @api.depends("lot_id", "lot_id.name")
    def _compute_supplier_number(self):
        for record in self:
            record.supplier_lot_number = record.lot_id.name

    @api.depends("lot_id")
    def _compute_supplier_product(self):
        for record in self:
            record.supplier_product_id = record.lot_id.product_id

    @api.depends("picking_id")
    def _compute_purchase(self):
        for rec in self:
            rec.purchase_id = rec.picking_id.purchase_id

    def _inverse_supplier_lot_number(self):
        for record in self:
            if record.lot_id:
                record.lot_id.write(
                    {
                        "name": record.supplier_lot_number or record.lot_id.name,
                        "product_id": record.supplier_product_id.id
                        or record.lot_id.product_id.id,
                    }
                )
            elif record.supplier_lot_number and record.supplier_product_id:
                lot = self.env["stock.production.lot"].search(
                    [
                        ("name", "=", record.supplier_lot_number),
                        ("product_id", "=", record.supplier_product_id.id),
                    ]
                )
                if lot:
                    record.lot_id = lot
                else:
                    record.lot_id = self.env["stock.production.lot"].create(
                        {
                            "name": record.supplier_lot_number,
                            "product_id": record.supplier_product_id.id,
                        }
                    )

    @api.constrains("picking_id", "purchase_id")
    def _check_picking_id(self):
        for rec in self:
            if rec.picking_id:
                if rec.picking_id.picking_type_id.code != "incoming":
                    raise ValidationError(
                        _(
                            "You have selected for the maintenance equipment %s the "
                            "picking %s, which is not an incoming picking."
                        )
                        % (rec.name, rec.picking_id.name)
                    )
                elif not rec.picking_id.purchase_id:
                    raise ValidationError(
                        _(
                            "You have selected for the maintenance equipment %s the "
                            "picking %s, which is not linked to any purchase."
                        )
                        % (rec.name, rec.picking_id.name)
                    )
                elif rec.purchase_id != rec.picking_id.purchase_id:
                    raise ValidationError(
                        _(
                            "You have selected for the maintenance equipment %s the "
                            "picking %s, which is not linked to the same purchase "
                            "you have selected."
                        )
                        % (rec.name, rec.picking_id.name)
                    )
            else:
                if rec.purchase_id:
                    raise ValidationError(
                        _(
                            "You have selected for the maintenance equipment %s a "
                            "purchase, but you have not selected any picking."
                        )
                        % rec.name
                    )

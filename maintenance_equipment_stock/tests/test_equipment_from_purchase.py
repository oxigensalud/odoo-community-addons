# Copyright 2023 Dixmit
# Copyright 2025 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestEquipmentFromPurchase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Demo Partner"})
        cls.product = cls.env["product.template"].create(
            {
                "name": "My Product",
                "is_storable": True,
                "tracking": "serial",
                "maintenance_lot": True,
            }
        )
        cls.purchase = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.product_variant_id.id,
                            "name": cls.product.name,
                        },
                    )
                ],
            }
        )
        cls.equipment_1 = cls.env["maintenance.equipment"].create({"name": "Laptop 1"})
        cls.location_1 = cls.env["stock.location"].create(
            {
                "name": "Test location 1",
                "usage": "internal",
                "location_id": cls.env.ref("stock.stock_location_stock").id,
            }
        )

    def test_equipment_creation(self):
        self.purchase.button_confirm()
        picking = self.purchase.picking_ids
        self.assertTrue(picking)
        picking.move_ids_without_package.move_line_ids.write(
            {
                "lot_name": "1234",
                "quantity": 1,
            }
        )
        self.assertFalse(picking.maintenance_equipment_ids)
        picking.button_validate()
        self.assertTrue(picking.maintenance_equipment_ids)
        without_package = picking.move_ids_without_package
        action = without_package.move_line_ids.lot_id.action_lot_open_equipment()
        self.assertEqual(
            picking.maintenance_equipment_ids,
            self.env[action["res_model"]].browse(action["res_id"]),
        )

    def test_equipment_location(self):
        self.equipment_1.stock_location_id = self.location_1.id
        self.assertEqual(self.location_1.equipment_ids.id, self.equipment_1.id)

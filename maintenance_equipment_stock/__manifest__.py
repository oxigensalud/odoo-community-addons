# Copyright 2023 Dixmit
# Copyright 2025 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Stock",
    "summary": """
        Create equipments from stocks""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit, Oxigen Salud SA, NuoBiT Solutions SL",
    "website": "https://github.com/oxigensalud/odoo-community-addons",
    "depends": [
        "maintenance",
        "purchase_stock",
        "product_brand",
    ],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_lot_views.xml",
        "views/stock_location_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/product_template_views.xml",
    ],
}

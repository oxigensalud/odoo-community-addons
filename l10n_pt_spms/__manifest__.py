# Copyright 2023 Dixmit
# Copyright 2025 NuoBiT - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


{
    "name": "SPMS base",
    "summary": "SPMS base models and fields",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit, NuoBiT Solutions S.L.",
    "website": "https://github.com/oxigensalud/odoo-community-addons",
    "depends": ["account"],
    "data": [
        "views/res_partner.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/spms_context_views.xml",
        "views/spms_prescription_type_views.xml",
        "views/spms_lot_views.xml",
        "views/product_template_views.xml",
        "views/spms_suspension_reason_views.xml",
    ],
}

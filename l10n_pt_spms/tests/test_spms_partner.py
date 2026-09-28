# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, tagged
from odoo.tests.common import SavepointCase


@tagged("post_install", "-at_install")
class TestSpmsPartner(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.portuguese_company = cls.env["res.company"].create(
            {
                "name": "SPMS Portuguese test company",
                "country_id": cls.env.ref("base.pt").id,
            }
        )
        cls.spanish_company = cls.env["res.company"].create(
            {
                "name": "SPMS Spanish test company",
                "country_id": cls.env.ref("base.es").id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {"name": "SPMS shared test customer"}
        )
        for company in cls.portuguese_company + cls.spanish_company:
            for kind in ("receivable", "payable"):
                account = (
                    cls.env["account.account"]
                    .with_company(company)
                    .create(
                        {
                            "name": "SPMS test " + kind,
                            "code": "SP" + kind.upper(),
                            "company_id": company.id,
                            "reconcile": True,
                            "user_type_id": cls.env.ref(
                                "account.data_account_type_" + kind
                            ).id,
                        }
                    )
                )
                cls.partner.with_company(company)[
                    "property_account_" + kind + "_id"
                ] = account

    def test_checkbox_available_in_portuguese_company(self):
        partner = self.partner.with_company(self.portuguese_company)
        with Form(partner) as form:
            self.assertFalse(form._get_modifier("spms_information", "invisible"))
            form.spms_information = True
        self.assertTrue(partner.spms_information)

    def test_checkbox_hidden_in_spanish_company(self):
        partner = self.partner.with_company(self.spanish_company)
        form = Form(partner)
        self.assertTrue(form._get_modifier("spms_information", "invisible"))

    def test_company_switch_keeps_shared_partner_information(self):
        partner = self.partner.with_company(self.portuguese_company)
        with Form(partner) as form:
            form.spms_information = True
        spanish_form = Form(partner.with_company(self.spanish_company))
        self.assertTrue(spanish_form._get_modifier("spms_information", "invisible"))
        self.assertTrue(partner.spms_information)
        self.assertTrue(Form(partner).spms_information)

import random

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    test_field = fields.Char(
        string='Test',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    responsible_for_issuing = fields.Many2one(
        'hr.employee',
        string='Ответственный за выдачу товара',
        required=True,
    )

    def _generate_ten_random_chars(self) -> str:
        return ''.join(random.choices(
            [chr(num) for num in range(97, 123)], k=10)
        )

    @api.onchange('date_order', 'order_line')
    def _onchange_date_order_or_product_id(self) -> None:
        self.test_field = (
            str(self.amount_total) + ' - ' + str(self.date_order)
            if self.partner_id and self.responsible_for_issuing
            else self._generate_ten_random_chars()
        )

    @api.constrains('test_field')
    def _check_test_field(self) -> None or ValidationError:
        for record in self:
            if record.test_field and len(record.test_field) > 50:
                raise ValidationError(
                    'Длина текста должна быть меньше 50 символов!'
                )

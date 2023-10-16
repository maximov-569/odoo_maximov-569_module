import random

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _generate_ten_random_chars(self) -> str:
        return ''.join(random.choices(
            [chr(num) for num in range(97, 123)], k=10)
        )

    # Also can be used 'size' attribute to set max_length of test_field.
    test_field = fields.Char(
        string='Test',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=_generate_ten_random_chars
    )
    responsible_for_issuing = fields.Many2one(
        'hr.employee',
        string='Ответственный за выдачу товара',
        required=True,
    )

    @api.onchange('date_order', 'order_line')
    def _onchange_date_order_or_product_id(self) -> None:
        self.test_field = (
            str(self.amount_total) + ' - ' + str(self.date_order)
            if self.partner_id and self.responsible_for_issuing
            else self._generate_ten_random_chars()
        )

    # Onchange can be attached to constrains
    # but inputted text get missed with validation error.
    @api.onchange('test_field')
    def _onchange_check_len_of_test_field(self) -> None or dict[
                                                           str:dict[str:str]
                                                           ]:
        if len(self.test_field) > 50:
            return {
                'warning': {
                    'title': 'Length warning!',
                    'message': 'Длина текста должна быть меньше 50 символов!',
                }
            }

    @api.constrains('test_field')
    def _check_test_field(self) -> None or ValidationError:
        if self.test_field and len(self.test_field) > 50:
            raise ValidationError(
                'Длина текста должна быть меньше 50 символов!'
            )

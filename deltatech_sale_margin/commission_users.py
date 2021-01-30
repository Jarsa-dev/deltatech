# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com       
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api, tools, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp
from openerp.api import Environment


class commission_users(models.Model):
    _name = 'commission.users'
    _description = "Users commission"

    user_id = fields.Many2one('res.users', string='Salesperson', required=True)
    name = fields.Char(string='Name', related='user_id.name')
    rate = fields.Float(string="Rate", default=0.01, digits=(12,3))
    manager_rate = fields.Float(string="Rate manager", default=0, digits=(12,3))
    manager_user_id = fields.Many2one('res.users', string='Sales Manager')
    journal_id = fields.Many2one('account.journal', string='Journal',     domain="[('type', 'in', ['sale','sale_refund'])]")

    #commission_type = fields.Selection([('product', 'Stockable Product'),('consu', 'Consumable'), ('service', 'Service')], 'Product Type', default='product' )

    _constraints = [
        (models.Model._check_recursion,
         'Error ! You cannot create recursive.',
         ['mamager_user_id'])
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

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
#
##############################################################################


from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp

"""
class service_consumable(models.Model):
    _name = 'service.consumable'
    _description = "Consumable List"

    name = fields.Char(string='Name')
    categ = fields.Selection([('type', 'Type'), ('product', 'Product')])
    type_id = fields.Many2one('service.equipment.type', string="Type", ondelete='restrict', )
    product_id = fields.Many2one('product.product', string='Product', ondelete='restrict',
                                 domain=[('type', '=', 'product')])
    item_ids = fields.One2many('service.consumable.item', 'consumable_id', string='Consumable')


    @api.onchange('categ', 'type_id', 'product_id')
    def onchange_categ(self):
        if self.categ == 'type':
            self.name = self.type_id.name
        else:
            self.name = self.product_id.name


"""

class service_consumable_item(models.Model):
    _name = 'service.consumable.item'
    _description = "Consumable Item"

    name = fields.Char(string='Name', related='product_id.name')
    # consumable_id = fields.Many2one('service.consumable', string='Consumable List', ondelete='cascade')
    type_id = fields.Many2one('service.equipment.type', string="Type", ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Consumable', ondelete='restrict',
                                 domain=[('type', '=', 'product')])
    quantity = fields.Float(string='Quantity', compute='_compute_quantity',
                            digits=dp.get_precision('Product Unit of Measure'))
    shelf_life = fields.Float(string='Shelf Life', related='product_id.shelf_life')
    uom_shelf_life = fields.Many2one(string='Shelf Life UoM', related='product_id.uom_shelf_life')
    colors = fields.Char("HTML Colors Index", default="['#a9d70b', '#f9c802', '#ff0000']")
    max_qty = fields.Float(string='Quantity Max', digits=dp.get_precision('Product Unit of Measure'),
                           help="Maximum Quantity allowed")

    @api.one
    def _compute_quantity(self):
        equipment_id = self.env.context.get('equipment_id', False)
        if equipment_id:
            # old method - to delete if new method ok:
            # self.quantity = 0.0
            # if equipment_id:
            #     eff = self.env['service.efficiency.report']
            #     domain = [('product_id', '=', self.product_id.id), ('equipment_id', '=', equipment_id)]
            #     fields = ['equipment_id', 'product_id', 'location_dest_id', 'usage', 'shelf_life']
            #     groupby = ['equipment_id', 'product_id', 'location_dest_id']
            #     res = eff.read_group(domain=domain, fields=fields, groupby=groupby, lazy=False)
            #     quantity = 0.0
            #     for line in res:
            #         location_destination_id = self.env['stock.location'].browse(line['location_dest_id'][0])
            #         if location_destination_id.usage == 'internal':
            #             quantity +=  line['usage']
            #         else:
            #             quantity +=  -line['usage']
            #     if quantity:
            #         self.quantity = self.shelf_life + quantity
            picking_type_id = self.sudo().env.ref('stock.picking_type_outgoing_not2binvoiced').id
            pickings = self.env['stock.picking'].sudo().search(
                [('equipment_id', '=', equipment_id),
                 ('picking_type_id', '=', picking_type_id), ('state', '=', 'done')])
            move_lines = self.env['stock.move'].sudo().search([('picking_id', 'in', pickings.ids), ('product_id', '=', self.product_id.id)])
            move_qtys = 0.0
            for move in move_lines:
                if move.location_dest_id.usage == 'internal':
                    move_qtys += - move.product_id.shelf_life * move.product_uom_qty
                else:
                    move_qtys += move.product_id.shelf_life * move.product_uom_qty
            
            eff = self.env['service.efficiency.report']
            domain = [('product_id', '=', self.product_id.id), ('equipment_id', '=', equipment_id)]
            fields = ['equipment_id', 'product_id', 'location_dest_id', 'usage', 'shelf_life']
            groupby = ['equipment_id', 'product_id', 'location_dest_id']
            res = eff.read_group(domain=domain, fields=fields, groupby=groupby, lazy=False)
            usage = 0.0
            for line in res:
                # location_destination_id = self.env['stock.location'].browse(line['location_dest_id'][0])
                # if location_destination_id.usage != 'internal':
                usage = line['usage']
            self.quantity = move_qtys - usage
        
        
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

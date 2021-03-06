# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
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

import time
from openerp.osv import osv
from openerp.report import report_sxw

class eq_report_purchase_order(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(eq_report_purchase_order, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
            'get_qty':self.get_qty,
            'get_price': self.get_price,
            'get_standard_price': self.get_standard_price,
            'get_tax': self.get_tax,
        })
        
    def get_tax(self, object, tax_id, language, currency_id):
        amount_net = 0;
        for line in object.order_line:
            if tax_id.id in [x.id for x in line.taxes_id]:                
                 amount_net += line.price_subtotal
                 
        tax_amount = 0
        for tex in self.pool.get('account.tax')._compute(self.cr, self.uid, [tax_id], amount_net, 1):
            tax_amount += tex['amount']
            
        return self.pool.get("eq_report_helper").get_price(self.cr, self.uid, tax_amount, language, 'Sale Price Report', currency_id)
    
    def get_qty(self, object, language):
        return self.pool.get("eq_report_helper").get_qty(self.cr, self.uid, object, language, 'Purchase Quantity Report')
           
    
    def get_price(self, object, language, currency_id):                
        return self.pool.get("eq_report_helper").get_price(self.cr, self.uid, object, language, 'Purchase Price Report', currency_id)
    
    
    def get_standard_price(self, object, language, currency_id):
        return self.pool.get("eq_report_helper").get_standard_price(self.cr, self.uid, object, language, currency_id)
          
    
class report_lunchorder(osv.AbstractModel):
    _name = 'report.purchase.report_purchaseorder'
    _inherit = 'report.abstract_report'
    _template = 'purchase.report_purchaseorder'
    _wrapped_report_class = eq_report_purchase_order
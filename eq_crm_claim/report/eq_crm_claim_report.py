# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import models, fields, api, _
from openerp import tools

class eq_crm_claim_report(models.Model):
    
    _inherit = "crm.claim.report"
    _auto=False
    
    eq_costs = fields.Float('Costs')
    sub_categ_id = fields.Many2one('eq.crm.claim.sub.category', 
                                   'Sub-category', required=False)
    eq_waste_parts = fields.Float('Waste', group_operator="sum")#Ausschussteile
    eq_good_parts = fields.Float('Good parts', group_operator="sum")#"Gut-Teile"
    
    def init(self, cr):

        """ Display Number of cases And Section Name
        @param cr: the current row, from the database cursor,
         """
        
        tools.drop_view_if_exists(cr, 'crm_claim_report')
        cr.execute("""
            create or replace view crm_claim_report as (
                select
                    min(c.id) as id,
                    c.date as claim_date,
                    c.date_closed as date_closed,
                    c.date_deadline as date_deadline,
                    c.user_id,
                    c.stage_id,
                    c.section_id,
                    c.partner_id,
                    c.company_id,
                    c.categ_id,
                    c.sub_categ_id,
                    c.name as subject,
                    count(*) as nbr,
                    c.priority as priority,
                    c.type_action as type_action,
                    c.create_date as create_date,
                    c.eq_costs,
                    c.eq_waste_parts,
                    c.eq_good_parts,
                    avg(extract('epoch' from (c.date_closed-c.create_date)))/(3600*24) as  delay_close,
                    (SELECT count(id) FROM mail_message WHERE model='crm.claim' AND res_id=c.id) AS email,
                    extract('epoch' from (c.date_deadline - c.date_closed))/(3600*24) as  delay_expected
                from
                    crm_claim c
                group by c.date,\
                        c.user_id,c.section_id, c.stage_id,\
                        c.categ_id, c.sub_categ_id,c.partner_id,c.company_id,c.create_date,
                        c.priority,c.type_action,c.date_deadline,c.date_closed,c.id
            )""")
# -*- coding: utf-8 -*-

import logging
from odoo import models, api  
 
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'



    @api.multi
    def clean_internal_number(self):
        for rec in self:
            
            if 'document_sequence_id' in rec._fields and \
                    rec.document_sequence_id:
                rec.write({
                    'move_name': False,
                    'document_number': False})
            else:
                rec.write({'move_name': False})



 
class AccountInvoiceCancel(models.TransientModel):
    _name = 'account.invoice.cancel'
    _description = "Wizard - Account Invoice Force Delete"
    
  
  

    @api.multi
    def invoice_cancel(self):
   
        invoices = self._context.get('active_ids')
        invoices_id = self.env['account.invoice'].browse(invoices)
        save_any_credit_note =[] 
        count_invoice=0 
        count_credit_note=0  

        # informations  payment or creditNote  
        for payment_move_line in invoices_id:
            all_info_creditNote_and_payment  = payment_move_line._get_payments_vals()
            for info in all_info_creditNote_and_payment: 
                x =  info['account_payment_id']
                if  x  is False: 
                    save_any_credit_note.append(info['invoice_id'])  #append creditNote
               
                            
        # remove_move_reconcile payment & creditNote        
        for payment_move_line in invoices_id:
            payment_move_line.payment_move_line_ids.remove_move_reconcile() 
 
 
       # invoice 
        for invoice in invoices_id:
            invoice.update({'state':'draft'})
            invoice.action_invoice_cancel()


            invoice.clean_internal_number() 
            if invoice.unlink():
                count_invoice += 1
 
       #credit_note 
        for credit_note in save_any_credit_note:
            credit_note_id = self.env['account.invoice'].search([('id', '=', credit_note)], limit=1)
            credit_note_id.update({'state':'draft'})
            credit_note_id.action_invoice_cancel()
                 
            #delete
            credit_note_id.clean_internal_number()
            if credit_note_id.unlink():
                count_credit_note += 1 


        # Message
        return {
            'effect': {
                'fadeout': 'slow',
                'message': (  "Invoices deleted : (" +  str(count_invoice)   +    ") and "  +  "  Credit note deleted : ("  + str(count_credit_note) +")"        ) ,                                                                             
                'img_url': '/force_delete_multi_invoice-11.0/static/description/icon.png',
                'type': 'rainbow_man',
            }
        } 

    @api.multi
    def invoice_cancel2(self):
   
        invoices = self._context.get('active_ids')
        invoices_id = self.env['account.invoice'].browse(invoices)
        save_any_credit_note =[] 
        count_invoice=0 
        count_credit_note=0  

        # informations  payment or creditNote  
        for payment_move_line in invoices_id:
            all_info_creditNote_and_payment  = payment_move_line._get_payments_vals()
            for info in all_info_creditNote_and_payment: 
                x =  info['account_payment_id']
                if  x  is False: 
                    save_any_credit_note.append(info['invoice_id'])  #append creditNote
               
                            
        # remove_move_reconcile payment & creditNote        
        for payment_move_line in invoices_id:
            payment_move_line.payment_move_line_ids.remove_move_reconcile() 
 
 
       # invoice 
        for invoice in invoices_id:
            invoice.action_invoice_cancel() #cancel invoice
            count_invoice += 1
 
       #credit_note 
        for credit_note in save_any_credit_note:
            credit_note_id = self.env['account.invoice'].search([('id', '=', credit_note)], limit=1)
            credit_note_id.action_invoice_cancel() #credit note
            count_credit_note += 1 


        # Message
        return {
            'effect': {
                'fadeout': 'slow',
                'message': (  "Invoices Canceled : (" +  str(count_invoice)   +    ") and "  +  "  Credit note Canceled : ("  + str(count_credit_note) +")"        ) ,                                                                             
                'img_url': '/force_delete_multi_invoice-11.0/static/description/icon.png',
                'type': 'rainbow_man',
            }
        } 

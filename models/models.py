# -*- coding: utf-8 -*-

from time import time
from odoo import models, fields, api


## Task Category Model

class project_task_categories(models.Model):
    _name = 'task.category'
    _description = 'Task Categories'

    name = fields.Char(string='Task Category', required=True,
                       help='Task Category E.g. Design, Manufacturing , Security')
    code = fields.Char(string='Code', help='The Task Category code.', required=True)

    # active = fields.Binary(string=" Status ")


##



############# Timesheet Module

class TimesheetType(models.Model):
    _name = 'timesheet.type'
    _description = 'Timesheet Type'

    name = fields.Char(string='Timesheet Type', required=True,
                       help='Timesheet Type E.g. Development, Business Analysis , Project Management , Support')


#
class AccountAnalyticLineInherit(models.Model):
    # _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'

    timesheet_type = fields.Many2one('timesheet.type', string='Timesheet Type', required=True, store=True,
                                     help='Timesheet Type E.g. Development, Business Analysis , Project Management , Support')
    project_id = fields.Many2one('project.project')


    # @api.depends('project_id')
    # def _compute_task_id_with_state_Approved(self):
    #     for rec in self:
    #         task = self.env['project.task'].search(
    #             [('project_id', '=', rec.project_id.id), ('task_id', '=', rec.task_id1.id)])
    #         print('task' , task )
    #         print('task_id', task.id)
    #         rec.task_id1 = task.id
    #
    #         for rec in self:
    #             task = self.env['project.task'].search(
    #                 [('project_id', '=', rec.project_id.id), ('request_id', '=', rec.id)])
    #             rec.task_id = task.id


    # state = fields.Char('State', default='Submitted')
    state = fields.Selection([
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ], default='Submitted', string='State', readonly=True, store=True )

    action_done = fields.Char(default='Approve')
    action_reject = fields.Char(default='Reject')


   ## For access the whole record of 'task.category'
    project_task_category_id = fields.Many2one('task.category', required=True,
                                               help='Task Category E.g. Design, Manufacturing , Marketing , Security, COnstruction')

    ## For access the whole record of 'sla.rule'
    sla_rule_id = fields.Many2one('sla.rule', string='sla_rule_key',
                                  help='To access the fields in sla_rule model')
    ## Access Each record in sla.rule
    sla_time = fields.Float(string='SLA Time', related='sla_rule_id.sla_time')
    time_spent = fields.Float(related='sla_rule_id.time_spent', string='Time Spent')
    sla_status = fields.Selection([
        ('Breach SLA', 'Breach SLA'),
        ('Within SLA', 'Within SLA'),
    ], related='sla_rule_id.sla_status', string='SLA Rule Status', readonly=True)
    warning = fields.Float(string='Warning Time', related='sla_rule_id.warning')



    project_task_id = fields.Many2one('project.task', string="Project Task Id")

    @api.model
    def select_accepted(self, id):
        # print(self.state)

        # print(id)
        new_records = self.browse(id)
        # print(new_records)
        # print(new_records.state)
        # print(new_records.timesheet_type)
        # print(new_records.action_done)
        # print(new_records.action_reject)

        return self.env['account.analytic.line'].search([('id', 'in', id)]).write( {'state': 'Approved'} )


    @api.model
    def select_rejected(self , id):
        #new_records = self.browse(id)
        return self.env['account.analytic.line'].search([('id', 'in', id)]).write( {'state': 'Rejected'} )


    


    # this function is overriding create function
    @api.model
    def create(self, vals_list):

        rec = super(AccountAnalyticLineInherit, self).create(vals_list)
        return rec

        '''
        print('Attributes belonging to env are:', dir(self.env))
        print('..........................................'
              '.........................................'
              ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,'
              './///////////////////////////////')
        print( self.env )
        print(self.env.user)             ## res.users(1, )
        print(self.env.user.name)        ## Odoobot


        print(self.env.cr)
        print(self.env.company)
        print(self.env.company)
        print(self.env.lang)
        print(self.env.su)
        print(self.env.uid)
        print(self.env.cr)


        print(self.env.vals_list)  ## { name : 'ABC' , .........  }
        print(self.env.context)    ## { 'lang' : 'en_US' , 'tz' : False }
        context = self.env.context
        context['default_phone'] = '123456'
        print(context)

        self.env.cr.commit()
        partner_obj = self.env['res.partner']
        partner_obj.with_user( weblearn_user).create( {'name': 'Weblearns User Partner'})
        self.env.cr.commit()


        company_id2 = self.env['res.company'].browse(2)

        partner_obj.with_company( company_id2 ).create({'name': 'Weblearns User Partner'})
        print(rec)            ## res.partner( 13, )  if using res.partner model



### Create a record  with context information 
        ##partner_obj.with_context( context ).create( {'name': })


    
    new_cr = registry(self.env.cr.dbname).cursor()
    partner_id = self.env['res.partner'].with_env( self.env( cr = new_cr ) ).sudo()create( {'name': "New Env CR Partner "}
    partner_id.env.cr.commit()
    
    ## with_env
    ## with_company
    ## with_user
    ## sudo
        '''











        # print('vals_list' , vals_list)
        # print('rec:', rec)
        # print('project_id' , vals_list['project_id'])
        # print('task_id', vals_list['task_id'])

        # domain = [ ('project_id', '=', vals_list['project_id']) ,  ('timesheet_type', '=' , vals_list['timesheet_type'] ) , ('task_id', '=' , vals_list['task_id'] ) ]


        # matched_rec = self.env['account.analytic.line'].search( domain )
        # time = 0
        # #domain = ['|', ('product_id', 'in', products.ids), '&', ('product_id', '=', False), ('product_tmpl_id', 'in', products.product_tmpl_id.ids)]
        #
        # print('matched_rec: ' , matched_rec)
        #
        # for rec in matched_rec:
        #
        #     time += rec['unit_amount']
        #     print('matched_rec t1', rec['unit_amount'])
        # vals_list['time_spent'] = time
        # vals_list['warning'] = 10
        # if vals_list['warning']:
        #     if vals_list['warning'] < vals_list['time_spent']:
        #         print('Raise an Notification')
        #         vals_list['sla_status'] = 'Breach SLA'
        #     else:
        #         vals_list['sla_status'] = 'Within SLA'
        # print('modified_vals_list:' , vals_list)
        # print('rec', rec)



    '''
    @api.model_create_multi
    def message_test(self):
        print(self.switch_power)
        if (self.switch_power == '1'):
            self.switch_power = '0'
            #raise osv.except_osv(('Button test!'), ('Le button est on'))

        else:
            self.switch_power = '1'
            #raise osv.except_osv(('Button test!'), ('Le button est off'))

    @api.model_create_multi
    def accept_timesheet(self):
        self.ensure_one()
        pass
'''
    '''
    # @api.model_create_multi
    # def accept_timesheet(self, context={}):
    #     context = context or {}
    #     print(context)
    #     print(self)
    #     accepted_int = context.get('accepted_int')
    #     #accepted_int = 0
    #
    #     accepted_int += 1
    #     print(accepted_int)
    #     if (accepted_int % 2 != 0):
    #         super(Account_Analytic_Line_Inherit, self).write(
    #          {'state': 'Accepted'})
    #     else:
    #         super(Account_Analytic_Line_Inherit, self).write({'state': 'Submitted'})
    #     return self

    #     if accepted_boolean:
    #         accepted_boolean = False
    #     else:
    #         accepted_boolean = True
    #
    #     super(Account_Analytic_Line_Inherit, self).write({'state': 'Accepted'} if vals_list['isCustomer'] else {'customer_rank': 0})
    # return {
    #     'state': 'Accepted',
    #     'view_mode': 'form',
    #     'res_model': 'your.model.name',
    #     'views': [(False, 'form')],
    #     'type': 'ir.actions.act_window',
    #     'target': 'new',
    #     'context': {},
    # }

    # def write(self, vals):
    #     print(vals)
    # if 'accepted_boolean' in vals_list:
    #     super(Account_Analytic_Line_Inherit, self).write({'state': 'Accepted'} if vals_list['accepted_boolean'] else {'state': 'Submitted'})
    # if 'rejected_boolean' in vals_list:
    #     super(Account_Analytic_Line_Inherit, self).write({'state': 'Rejected'} if vals_list['rejected_boolean'] else {'state': 'Submitted'})
    # return super(Account_Analytic_Line_Inherit, self).write(vals_list)
    

    # @api.model
    # def reject_timesheet(self):
    #     pass
    #     #self.state = 'Rejected'
    # #     #self.write({'state': 'Rejected'})

    
    
    '''

    # @api.model_create_multi
    # def reject_timesheet(self):
    #     self.ensure_one()
    #     pass
        # return {
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'your.model.name',
        #     'views': [(False, 'form')],
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        #     'context': {},
        # }

    #
    # @api.model_create_multi
    # def get_update(self, cr, uid, ids, context='state'):
    #     order_line_obj = self.pool.get('sale.order.line')
    #     for order in self.browse(cr, uid, ids, context=context):
    #         for line in order.order_line:
    #             order_line_obj.write(cr, uid, [line.id], {'shop_no':val})
    #     return True



### SLA Rule

    class sla_rule(models.Model):
        _name = 'sla.rule'

        _description = 'SLA Rule Name '
    
        name  = fields.Char(string='SLA Rule Name', required=True,)

        sla_time = fields.Float(string='SLA Time')


        project_task_category_id = fields.Many2one('task.category',  required=True,
                                                   help='Task Category E.g. Design, Manufacturing , Marketing , Security, COnstruction')


        task_category = fields.Char(string='Task Category', store=True,
                                    help='Task Category E.g. Design, Manufacturing , Security',
                                    related='project_task_category_id.name')

        task_category_code = fields.Char(string='Code', help='The Task Category code.',
                                         related='project_task_category_id.code')

        timesheet_type = fields.Many2one('timesheet.type', string='Timesheet Type', required = True,
                                     help='Timesheet Type E.g. Development, Business Analysis , Project Management , Support')

        time_spent = fields.Float(string='Time Spent')

        sla_status = fields.Selection([
            ('Breach SLA', 'Breach SLA'),
            ('Within SLA', 'Within SLA'),
        ], string='SLA Rule Status', readonly=True)

        warning = fields.Float(string='Warning Time')

        #sla_status = fields.Char(string='SLA Rule Status', compute='_compute_sla_status')

        project_task_id = fields.Many2one('project.task', string="Project Task Id")

        # analytic_account_line_id = fields.Many2one('account.analytic.line' )
        #
        #
        # analytic_account_line_ids = fields.One2many('account.analytic.line', 'sla_rule_id', string='analytic_account_line_ids',
        #              help='To access the fields in account.analytic.line model')
        #
        # time_spent = fields.Float(related = 'analytic_account_line_id.time_spent', string='Time Spent')


class project_task_inherit_sla_rule_(models.Model):
     _inherit = 'project.task'

### For utilizing the fields of 'task.category' model  in  'project.task'  model

     project_task_category_id = fields.Many2one('task.category', string='Category',
                                                help='Task Category E.g. Design, Manufacturing , Marketing , Security, COnstruction')

     task_category = fields.Char(string='Task Category', required=True, store = True,
                        help='Task Category E.g. Design, Manufacturing , Security' ,  related= 'project_task_category_id.name' )

     task_category_code = fields.Char(string='Code', help='The Task Category code.', required=True , related= 'project_task_category_id.code' )


##### For utilizing the fields of 'timesheet.type' model    in  'project.task'  model

     timesheet_type = fields.Many2one('timesheet.type', string='Timesheet Type', required=True,
                                      help='Timesheet Type E.g. Development, Business Analysis , Project Management , Support')


##### For utilizing the fields of 'sla.rule' model    in  'project.task'  model

     sla_time = fields.Float(string='SLA Time', related='sla_rule_id.sla_time')
    #  time_spent = fields.Float(related='sla_rule_id.time_spent', string='Time Spent') 
     sla_status = fields.Selection([
         ('breach', 'Breach SLA'),
         ('within', 'Within SLA'),
     ], related='sla_rule_id.sla_status', string='SLA Rule Status', readonly=True)

     sla_rule_name = fields.Char(string='SLA Rule Name', related = 'sla_rule_id.name')

     sla_time = fields.Float(string='SLA Time' , related = 'sla_rule_id.sla_time')
     warning = fields.Float(string='Warning Time' , related = 'sla_rule_id.warning' )
     sla_rule_id = fields.Many2one('sla.rule',
                                   help='To relate the Fields of the "sla rule model" in this module use Many2one Field ')

     sla_rule_ids = fields.One2many('sla.rule', 'project_task_id', string='sla_rule_key',
                     help='To access the fields in sla_rule model', compute = '_compute_sla_rule_ids')
    


     # compute='compute_overall_time_spent',
     overall_time_spent = fields.Float( string="Overall Time Spent",
                                       help="Overall time spent for a task and on all Timesheets Types", compute = "_compute_overall_time_spent")
     # compute='compute_overall_sla_time',
     overall_sla_time = fields.Float( string="Overall SLA Time",
                                     help="Overall SLA time assigned for a task and on  all Timesheets Types", compute="_compute_overall_sla_time")

     # def compute_overall_sla_time(self):
     #     pass
     # def compute_overall_time_spent(self):
     #     pass

     ##### For utilizing the fields of 'account.analytic.line' model    in  'project.task'  model   for making VIEWs and Pages
     analytic_account_line_ids = fields.One2many('account.analytic.line', 'project_task_id', string='analytic_account_line_ids',
                     help='To access the fields in account.analytic.line model')


### These are recent added

     analytic_account_line_id = fields.Many2one('account.analytic.line' )

     state = fields.Selection([
         ('Submitted', 'Submitted'),
         ('Approved', 'Approved'),
         ('Rejected', 'Rejected'),
     ], default='Submitted', string='State', store=True,   readonly=True )

     # time_spent = fields.Float(related='analytic_account_line_id.time_spent', string='Time Spent')

     def get_approved(self):
        return {
            'type': 'ir.actions.act_window',
            'name': ('Approved Timesheets'),
            'view_mode': 'tree',
            'view_id': self.env.ref('modification.hr_timesheet_tree_inherit').id,
            'res_model': 'account.analytic.line',
            'domain': [('task_id', '=', self.id),('state','=','Approved')],
            'target': 'new',
        }
    
     @api.depends('sla_rule_id')
     def _compute_overall_sla_time(self):
        
        sla_rules = self.env['sla.rule'].search([('project_task_category_id','=',self.project_task_category_id.id)])

        total_time = 0

        for rule in sla_rules:
            total_time += rule.sla_time
        
        self.overall_sla_time = total_time
    

     @api.depends('timesheet_ids')
     def _compute_overall_time_spent(self):
        timesheets = self.env['account.analytic.line'].search([('task_id','=',self.id),('state','=','Approved')])
        total_time = 0
        for timesheet in timesheets:
            total_time += timesheet.unit_amount
        self.overall_time_spent = total_time
            
     @api.depends('sla_rule_ids.project_task_id')
     def _compute_sla_rule_ids(self):
        for task in self:
            task.sla_rule_ids = self.env['sla.rule'].search([('project_task_category_id','=',task.project_task_category_id.id)])
            for rec in task.sla_rule_ids:
                timesheet = self.env['account.analytic.line'].search([('task_id','=',task.id),('state','=','Approved'),('timesheet_type','=',rec.timesheet_type.id)])
                print(timesheet) 

            
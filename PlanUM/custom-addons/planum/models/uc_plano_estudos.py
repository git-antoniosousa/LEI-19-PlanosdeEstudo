from odoo import fields, models

class UC_Plano_Estudos (models.Model):
    _inherit = 'planum.uc_plano_curso'
    _name='planum.uc_plano_estudos'
    _description='Unidade Curricular'
    _order='ano_conclusao asc'
    active = fields.Boolean('Active?', default=True)

    nota=fields.Integer('Nota')
    ano_conclusao=fields.Integer('Ano de Conclusão')
    plano_estudos_id=fields.Many2one('planum.plano_estudos', 'ID UC Plano Estudos')
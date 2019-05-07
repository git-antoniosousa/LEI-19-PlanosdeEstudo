from odoo import fields, models

class UC_Plano_Curso (models.Model):
    _name='planum.uc_plano_curso'
    _description='Unidade Curricular'
    _order='ano,semestre asc'
    active = fields.Boolean('Active?', default=True)

    codigo_plano=fields.Char('Código UC no Plano')
    ano=fields.Selection([(1,'1º ano'),(2,'2º ano'),(3,'3º ano'),(4,'4º ano'),(5,'5º ano'),(6,'6º ano')])
    semestre=fields.Selection([(1,'1º semestre'),(2,'2º semestre')], default=1)
    fator=fields.Float('Fator',(2,1))
    plano_curso_id=fields.Many2one('planum.plano_curso', 'Plano de Curso ID')
    docentes = fields.Many2many('planum.docente', 'Docentes')
    uc_id=fields.Many2one('planum.uc', 'UC ID')
    ucs_plano_estudos = fields.One2many('planum.uc_plano_estudos', 'uc_plano_curso_id', 'UCs de Planos de Estudos')
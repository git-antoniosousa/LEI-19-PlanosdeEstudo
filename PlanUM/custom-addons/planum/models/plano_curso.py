from odoo import fields, models

class Plano_Curso(models.Model):
    _name = 'planum.plano_curso'
    _description = 'Plano de Curso'
    _order = 'data_inicio desc'
    active = fields.Boolean('Active?', default=True)

    data_inicio=fields.Date('Data Inicio')
    data_fim = fields.Date('Data Fim')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')
    ucs = fields.One2many('planum.uc_plano_curso', 'plano_curso_id', 'Unidades Curriculares')
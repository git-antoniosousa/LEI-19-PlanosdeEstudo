from odoo import fields, models, api

class Estatistica(models.Model):
    _name = 'planum.estatistica'
    _description = 'Estatistica'
    active = fields.Boolean('Active?', default=True)

    ano = fields.Char('Ano')
    aprovados = fields.Integer('Aprovados')
    reprovados = fields.Integer('Reprovados')
    uc_plano_curso_id = fields.Many2one('planum.uc_plano_curso', 'UC Plano Curso ID')
from odoo import fields, models, api

class Previsao (models.Model):
    _name = 'planum.previsao'
    _description = 'Previsão'
    active = fields.Boolean('Active?', default=True)

    ano = fields.Char('Ano')
    min = fields.Integer('Inscrições Mínimas')
    med = fields.Float('Inscrições Médias',(5,2))
    max = fields.Integer('Inscrições Máximas')
    uc_plano_curso_id = fields.Many2one('planum.uc_plano_curso', 'ID UC Plano Curso')
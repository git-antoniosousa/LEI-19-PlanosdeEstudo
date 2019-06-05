from odoo import fields, models, api

class Previsao (models.Model):
    _name = 'planum.previsao'
    _description = 'Previsão'
    active = fields.Boolean('Active?', default=True)

    ano = fields.Char('Ano')
    #TODO Mudar para maximo e para minimo
    possiveis = fields.Integer('Inscrições Possíveis')
    garantidas = fields.Integer('Inscrições Garantidas')
    uc_plano_curso_id = fields.Many2one('planum.uc_plano_curso', 'ID UC Plano Curso')
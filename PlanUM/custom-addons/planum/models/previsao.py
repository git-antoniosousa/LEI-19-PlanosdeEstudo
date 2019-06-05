from odoo import fields, models, api

class Previsao (models.Model):
    _name = 'planum.previsao'
    _description = 'Previsão'
    active = fields.Boolean('Active?', default=True)

    ano = fields.Char('Ano')
    possiveis = fields.Integer('Inscrições Possíveis')
    garantidas = fields.Integer('Inscrições Garantidas')
    ano_letivo_id = fields.Many2one('planum.ano_letivo', 'ID Ano Letivo')
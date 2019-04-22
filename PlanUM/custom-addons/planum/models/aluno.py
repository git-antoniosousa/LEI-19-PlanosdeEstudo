from odoo import fields, models

class Aluno(models.Model):
    _inherit='res.partner'
    _name = 'planum.aluno'
    _description = 'Aluno'
    _order = 'nome desc'
    active = fields.Boolean('Active?', default=True)

    nome=fields.Char('Nome')
    nr_mecanografico=fields.Char('Nº Mecanográfico')
    media_acesso=fields.Float('Média Acesso',(5,3))
    estatuto=fields.Char('Estatuto')
    #Tirar?
    #regime=fields.Char('Regime')
    ano = fields.Integer('Ano')
    plano_estudos_id = fields.Many2one('planum.plano_estudos', 'Plano Estudos ID')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')
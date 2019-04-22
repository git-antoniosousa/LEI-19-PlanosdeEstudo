from odoo import fields, models

class Docente(models.Model):
    #Verificar se é partner ou user
    _inherit = 'res.partner'
    _name = 'planum.docente'
    _description = 'Docente'
    _order = 'nome desc'
    active = fields.Boolean('Active?', default=True)

    nome=fields.Char('Nome')
    nr_mecanografico = fields.Char('Nº Mecanográfico')
    ucs=fields.Many2many('planum.uc_plano_curso','UnidadesCurriculares')
    direcoes_curso=fields.Many2many('planum.direcao_curso', 'DirecoesCurso')
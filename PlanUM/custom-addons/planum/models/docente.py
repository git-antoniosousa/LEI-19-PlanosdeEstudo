from odoo import fields, models, api

class Docente(models.Model):
    _inherit = 'res.partner'
    _name = 'planum.docente'
    _description = 'Docente'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    name=fields.Char('Nome')
    nr_mecanografico = fields.Char('Nº Mecanográfico')
    ucs=fields.Many2many('planum.uc_plano_curso','UnidadesCurriculares')
    direcoes_curso=fields.Many2many('planum.direcao_curso', 'DirecoesCurso')

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True
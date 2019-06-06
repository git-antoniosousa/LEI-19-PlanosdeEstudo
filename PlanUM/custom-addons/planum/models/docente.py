from odoo import fields, models, api

class Docente(models.Model):
    _inherits = {'res.users': 'user_id'}
    _name = 'planum.docente'
    _description = 'Docente'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    ucs=fields.Many2many('planum.uc_plano_curso',string='UnidadesCurriculares')
    direcoes_curso=fields.Many2many('planum.direcao_curso', string='DirecoesCurso')

    @api.model
    def create(self, vals):
        vals['login'] = vals['nr_mecanografico']
        # Arranjar maneira de dar password?
        vals['password'] = "temp"
        new_record = super().create(vals)
        security_group = self.env.ref('planum.planum_group_docente')
        security_group.write({
            'users': [(4,new_record.user_id.id)]
        })
        return new_record

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True
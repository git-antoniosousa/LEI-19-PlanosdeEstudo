from odoo import fields, models, api

class Aluno(models.Model):
    _inherit='res.partner'
    _name = 'planum.aluno'
    _description = 'Aluno'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    name=fields.Char('Nome')
    nr_mecanografico=fields.Char('Nº Mecanográfico')
    media_acesso=fields.Float('Média Acesso',(5,3))
    estatuto=fields.Char('Estatuto')
    ano = fields.Integer('Ano')
    plano_estudos_id = fields.Many2one('planum.plano_estudos', 'Plano Estudos ID')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')

    @api.model
    def create(self, vals):
        curso_id = vals['curso_id']
        curso = self.env['planum.curso'].browse(curso_id)
        uc_plano_estudos = self.env['planum.uc_plano_estudos']
        plano_curso=self.env['planum.plano_curso'].browse(curso.plano_atual())

        # Criar plano de estudos e UCs plano estudo
        plano_estudos = self.env['planum.plano_estudos'].create({
            'media_licenciatura': 0,
            'media_parcial': 0
        })

        for uc in plano_curso.ucs:
            new_uc = uc_plano_estudos.create({
                'nota':0,
                'ano_conclusao':0,
                'plano_estudos_id':plano_estudos.id,
                'uc_plano_curso_id':uc.id,
            })



        # Define plano de estudos
        vals['plano_estudos_id'] = plano_estudos.id

        new_record = super().create(vals)

        # Add security group to aluno
        security_group = self.env.ref('planum.planum_group_aluno')
        security_group.write({
            'users': [(4, res.user_id.id)]
        })

        return new_record

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True
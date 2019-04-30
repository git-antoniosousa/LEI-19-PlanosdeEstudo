from odoo import fields, models, api

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
    ano = fields.Integer('Ano')
    plano_estudos_id = fields.Many2one('planum.plano_estudos', 'Plano Estudos ID')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')

    @api.model
    def create(self, vals):
        curso_id = vals['curso_id']
        curso = self.env['planum.curso'].browse(curso_id)

        # Define plano de estudos
        vals['plano_estudos_id'] = curso.plano_atual()

        new_record = super().create(vals)

        # Add security group to aluno
        security_group = self.env.ref('planum.planum_group_aluno')
        security_group.write({
            'users': [(4, res.user_id.id)]
        })

        return new_record
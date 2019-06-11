from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Aluno(models.Model):
    _inherits ={'res.users': 'user_id'}
    _name = 'planum.aluno'
    _description = 'Aluno'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    media_acesso = fields.Float('Média Acesso',(5,3))
    estatuto = fields.Selection([(1,'Estudante'),(2,'Estudante Trabalhador'),(3,'Estudante Atleta')], default=1)
    ano = fields.Selection([(1,'1º ano'),(2,'2º ano'),(3,'3º ano'),(4,'4º ano'),(5,'5º ano'),(6,'6º ano')], default=1)
    plano_estudos_id = fields.Many2one('planum.plano_estudos', 'Plano Estudos ID')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')

    @api.multi
    def mudar_password(self):
        view_id = self.env.ref('planum.view_form_passowrd').id
        context = self._context.copy()

        return {
            'name': 'Mudar Password',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'planum.aluno',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': context,
        }

    @api.model
    def create(self, vals):
        # Verificar nº mecanográfico
        if not vals['nr_mecanografico']:
            raise ValidationError('O nome, o nº mecanográfico, o curso e o ano são campos obrigatórios.')

        curso_id = vals['curso_id']
        curso = self.env['planum.curso'].browse(curso_id)
        uc_plano_estudos = self.env['planum.uc_plano_estudos']
        plano_curso_id = curso.plano_atual()
        ano_atual = self.env['planum.ano_letivo'].search([]).ano

        plano_curso = self.env['planum.plano_curso'].browse(plano_curso_id)

        # Criar plano de estudos e UCs plano estudo
        plano_estudos = self.env['planum.plano_estudos'].create({})

        for uc in plano_curso.ucs:
            if uc.ano == 1:
                uc_plano_estudos.create({
                    'nota': 0,
                    'ano_conclusao': ano_atual,
                    'plano_estudos_id': plano_estudos.id,
                    'uc_plano_curso_id': uc.id
                })
            else:
                uc_plano_estudos.create({
                    'nota': 0,
                    'ano_conclusao': '',
                    'plano_estudos_id': plano_estudos.id,
                    'uc_plano_curso_id': uc.id,
                })

        # Define plano de estudos
        vals['plano_estudos_id'] = plano_estudos.id
        # Login
        vals['login'] = vals['nr_mecanografico']
        # Arranjar maneira de dar password?
        vals['password'] = vals['nr_mecanografico']
        new_record = super().create(vals)

        security_group = self.env.ref('planum.planum_group_aluno')
        security_group.write({
            'users': [(4, new_record.user_id.id)]
        })

        return new_record

    @api.constrains('curso_id', 'ano', 'nr_mecanografico')
    def aluno_check(self):
        if not self.curso_id.id or not self.ano:
            raise ValidationError('O nome, o nº mecanográfico, o curso e o ano são campos obrigatórios.')

        curso = self.env['planum.curso'].browse(self.curso_id.id)
        plano_curso_id = curso.plano_atual()[0]

        # Lançar erro se não existir um plano de curso ativo
        if not plano_curso_id:
            raise ValidationError(
                'O curso selecionado não possui um plano de curso ativo. Selecione outro curso ou tente '
                'novamente mais tarde.')

        if not self.env['planum.ano_letivo'].search([]).ano:
            raise ValidationError(
                'Não existe nenhum ano letivo criado. Tente novamente mais tarde.')

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True

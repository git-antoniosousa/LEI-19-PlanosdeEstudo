from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Aluno(models.Model):
    _inherits ={'res.users' : 'user_id'}
    _name = 'planum.aluno'
    _description = 'Aluno'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    nr_mecanografico=fields.Char('Nº Mecanográfico')
    media_acesso=fields.Float('Média Acesso',(5,3))
    estatuto=fields.Selection([(1,'Estudante'),(2,'Estudante Trabalhador'),(3,'Estudante Atleta')], default=1)
    ano = fields.Selection([(1,'1º ano'),(2,'2º ano'),(3,'3º ano'),(4,'4º ano'),(5,'5º ano'),(6,'6º ano')])
    plano_estudos_id = fields.Many2one('planum.plano_estudos', 'Plano Estudos ID')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')

    @api.model
    def create(self, vals):
        curso_id = vals['curso_id']
        vals['ano']=1
        curso = self.env['planum.curso'].browse(curso_id)
        uc_plano_estudos = self.env['planum.uc_plano_estudos']
        plano_curso_id=curso.plano_atual()
        ano_atual = self.env['planum.ano_letivo'].search([]).ano

        plano_curso=self.env['planum.plano_curso'].browse(plano_curso_id)

        # Criar plano de estudos e UCs plano estudo
        plano_estudos = self.env['planum.plano_estudos'].create({})

        for uc in plano_curso.ucs:
            if uc.ano == 1:
                uc_plano_estudos.create({
                    'nota': 0,
                    # ONDE GUARDAR O ANO LETIVO
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
        vals['login'] = vals['nr_mecanografico']
        # Arranjar maneira de dar password?
        vals['password'] = "temp"
        new_record = super().create(vals)

        security_group = self.env.ref('planum.planum_group_aluno')
        security_group.write({
            'users': [(4,new_record.user_id.id)]
        })

        return new_record

    @api.constrains('curso_id')
    def plano_curso_check(self):
        if not self.curso_id.id:
            raise ValidationError(
                'O aluno deve ter um curso a si associado.')

        curso = self.env['planum.curso'].browse(self.curso_id.id)
        plano_curso_id = curso.plano_atual()

        # Lançar erro se não existir um plano de curso ativo
        if plano_curso_id == [None]:
            raise ValidationError(
                'O curso selecionado não possui um plano de curso ativo. Selecione outro curso ou tente '
                'novamente mais tarde.')

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True
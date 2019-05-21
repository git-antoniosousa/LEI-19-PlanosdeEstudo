from odoo import fields, models, api

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
        curso = self.env['planum.curso'].browse(curso_id)
        uc_plano_estudos = self.env['planum.uc_plano_estudos']
        plano_curso_id=curso.plano_atual()

        #Corrigir erro do odoo neste caso, fazer rollback do create do aluno
        if plano_curso_id == [None]:
            print("Não há plano de curso para o curso selecionado")
            return
        plano_curso=self.env['planum.plano_curso'].browse(plano_curso_id)

        # Criar plano de estudos e UCs plano estudo
        plano_estudos = self.env['planum.plano_estudos'].create({})

        for uc in plano_curso.ucs:
            uc_plano_estudos.create({
                'nota':0,
                'ano_conclusao':0,
                'plano_estudos_id':plano_estudos.id,
                'uc_plano_curso_id':uc.id,
            })

        # Define plano de estudos
        vals['plano_estudos_id'] = plano_estudos.id
        vals['login'] = vals['name']
        # Arranjar maneira de dar password?
        vals['password'] = "temp"
        new_record = super().create(vals)

        security_group = self.env.ref('planum.planum_group_aluno')
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
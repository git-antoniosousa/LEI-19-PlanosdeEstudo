from odoo import fields, models, api

class UC_Plano_Curso (models.Model):
    _name = 'planum.uc_plano_curso'
    _description = 'Unidade Curricular'
    _order = 'ano,semestre asc'
    _rec_name = 'codigo_designacao'
    active = fields.Boolean('Active?', default=True)

    codigo_plano = fields.Char('Código UC no Plano')
    ano = fields.Selection([(1,'1º ano'),(2,'2º ano'),(3,'3º ano'),(4,'4º ano'),(5,'5º ano'),(6,'6º ano')])
    semestre = fields.Selection([(1,'1º semestre'),(2,'2º semestre')], default=1)
    fator = fields.Float('Fator',(2,1), default=1.0)
    plano_curso_id = fields.Many2one('planum.plano_curso', string='Plano de Curso ID')
    docentes = fields.Many2many('planum.docente', string='Docentes')
    uc_id = fields.Many2one('planum.uc', 'UC ID')
    ucs_plano_estudos = fields.One2many('planum.uc_plano_estudos', 'uc_plano_curso_id', 'UCs de Planos de Estudos')
    designacao = fields.Char('Designação', related='uc_id.designacao')
    ects = fields.Integer('Créditos ECTS', related='uc_id.ects')
    obrigatoria = fields.Boolean('Obrigatória?', related='uc_id.obrigatoria')
    codigo_designacao = fields.Char(compute='_compute_codigo_designacao')

    aprovados = fields.Integer(compute='_compute_aprovacoes')
    reprovados = fields.Integer(compute='_compute_aprovacoes')

    @api.depends('ucs_plano_estudos')
    def _compute_aprovacoes(self):
        for uc_plano_curso in self:
            aprovados = 0
            reprovados = 0
            for uc in uc_plano_curso.ucs_plano_estudos:
                if uc.ano_conclusao == '2018/2019':
                    if uc.nota >= 10:
                        aprovados += 1
                    if uc.nota < 10:
                        reprovados += 1
            uc_plano_curso.aprovados = aprovados
            uc_plano_curso.reprovados = reprovados

    @api.depends('codigo_plano', 'designacao')
    def _compute_codigo_designacao(self):
        for uc in self:
            uc.codigo_designacao = uc.codigo_plano + ' - ' + uc.designacao
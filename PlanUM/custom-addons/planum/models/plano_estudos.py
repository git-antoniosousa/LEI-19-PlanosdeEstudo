from odoo import fields, models, api

class Plano_Estudos (models.Model):
    _name = 'planum.plano_estudos'
    _description = 'Plano de Estudos'
    _order = 'id desc'
    _rec_name = 'aluno_nr'
    active = fields.Boolean('Active?', default=True)

    #media_parcial=fields.Float('Média Parcial',(5,3))
    media_licenciatura=fields.Float('Média Licenciatura',(5,3))
    ucs=fields.One2many('planum.uc_plano_estudos', 'plano_estudos_id', 'Unidades Curriculares')
    aluno=fields.One2many('planum.aluno', 'plano_estudos_id', 'Aluno')
    aluno_nr = fields.Char('Nº Aluno', related='aluno.nr_mecanografico')

    media_parcial=fields.Float(compute='_compute_media_parcial')

    @api.depends('ucs')
    def _compute_media_parcial(self):
        for p in self:
            p.media_parcial = 0
            total = 0
            i = 0
            for uc in self.ucs:
                if uc.nota != 0:
                    total += uc.nota
                    i+=1
            if total != 0:
                p.media_parcial = total/float(i)
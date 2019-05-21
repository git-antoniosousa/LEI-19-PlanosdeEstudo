from odoo import fields, models, api

class Plano_Estudos (models.Model):
    _name = 'planum.plano_estudos'
    _description = 'Plano de Estudos'
    _order = 'id desc'
    _rec_name = 'aluno_nr'
    active = fields.Boolean('Active?', default=True)

    #media_parcial=fields.Float('Média Parcial',(5,3))
    ucs=fields.One2many('planum.uc_plano_estudos', 'plano_estudos_id', 'Unidades Curriculares')
    aluno=fields.One2many('planum.aluno', 'plano_estudos_id', 'Aluno')
    aluno_nr = fields.Char('Nº Aluno', related='aluno.nr_mecanografico')

    media_parcial=fields.Float(compute='_compute_medias')
    media_licenciatura=fields.Float(compute='_compute_medias')

    @api.depends('ucs')
    def _compute_medias(self):
        for p in self:
            total_p = 0
            i_p = 0
            total_l = 0
            i_l = 0

            for uc in self.ucs:
                if uc.nota != 0:
                    total_p += uc.nota
                    i_p+=1
                if uc.ano < 4:
                    total_l += uc.nota
                    i_l+=1

            if total_p != 0:
                p.media_parcial = total_p/float(i_p)
            else:
                p.media_parcial = 0
            if total_l != 0:
                p.media_licenciatura = total_l/float(i_l)
            else:
                p.media_licenciatura = 0
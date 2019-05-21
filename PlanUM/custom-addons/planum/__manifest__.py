# -*- coding: utf-8 -*-
{
    'name': "PlanUM",

    'description': """
    	Módulo responsável pela gestao de planos de estudo 
        dos alunos da Universidade do Minho.
    """,

    'author': "Universidade do Minho",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'security/planum_security.xml',
        'security/ir.model.access.csv',
        'views/planum_menu.xml',
        'views/aluno_view.xml',
        'views/plano_estudos_view.xml',
        'views/curso_view.xml',
        'views/docente_view.xml',
        'views/plano_curso_view.xml',
        'views/uc_view.xml',
        'views/direcao_curso_view.xml',
        'views/uc_plano_estudos_view.xml',
        'views/uc_plano_curso_view.xml',
        'views/administrador_view.xml',
    ],

    # the module should be featured as an app in the apps list
    'application': True,

    # Install automatically
    'auto_install': True,
}

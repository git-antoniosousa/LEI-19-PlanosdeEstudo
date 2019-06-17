# PlanUM

Aplicação que pode ser utilizada tanto por docentes como por alunos da Universidade do Minho, para gerirem os planos de estudo e preverem antecipadamente os horários e necessidades letivas para o ano letivo seguinte.

# Instruções de setup

## Criar base de dados PostgreSQL

### Instalar o PostgreSQL

```
$ sudo apt update
$ sudo apt install postgresql # Instalar PostgreSQL
$ sudo su -c "createuser -s $USER" postgres # Criar superuser da bd
$ createdb planum # Criar bd
```

## Ativar o virtual environment

```
$ source odoo12env/bin/activate
```

## Instalar dependências

```
$ sudo apt install python3-dev python3-pip
$ sudo apt install build-essential libxslt-dev libldap2-dev libsasl2-dev libssl-dev
$ pip3 install -r odoo/requirements.txt
$ pip3 install num2words phonenumbers psycopg2-binary watchdog xlwt
```

## Iniciar aplicação

```
$ odoo/odoo-bin -d planum -i base -i auth_signup_register_and_reset -i planum --addons-path="odoo/addons,custom-addons" --save
```

## Configurar Odoo

No browser aceder a ```http://localhost:8069``` e fazer login com o email e a passowrd ```admin```.

### Ativar developer mode

Ir a **Settings | Dashboard** e no canto inferior direito clicar em **Activate the developer mode**.

### Configurar outgoing mail server

Ir a **Settings | Technical | Outgoing Mail Servers** e preencher o formulário.
No caso do Gmail, pode ser utilizada a seguinte configuração:
- **Description:** Gmail
- **Priority:** 1
- **SMTP Server:** smtp.gmail.com
- **SMTP Port:** 465
- **Connection Security:** SSL/TLS
- **Username:** *email*
- **Username:** *password*

Neste caso *email* e *password* dizem respeito às credenciais de uma conta Gmail previamente criada.

No fim deve-se clicar em **Test Connection** para garantir que a conexão é estabelecida com sucesso.

### Definir reset da passowrd através de email

Ir a **Apps**, remover o filtro *Apps* da pesquisa, pesquisar pelo módulo *Register and reset password* e instalá-lo.

De seguida é necessário ir a **Settings | General Settings**, marcar a opção **Password Reset** em **Users** e guardar.

### Configurar company

Ir a **Settings | Dashboard** e fazer o **Set up** de *YourCompany*.

Clicar em **Edit** para editar o formulário e preencher os campos pretendidos. O logotipo da aplicação encontra-se em ```PlanUM/custom-addons/planum/static/description/icon.png```.

### Criar administrador

Ir a **PlanUM | Administradores**, clicar em **Create** e preencher o formulário. Assim que clicar em **Save** ao novo administrador um email com o link para fazer o reset da password.

A partir daqui a aplicação poderá ser utilizada normalmente de acordo com o manual de utilização.

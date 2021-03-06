# -*- encoding: utf-8 -*-
import os
import sys

# BB_HOME points to installation folder of bridge builder
BB_HOME = os.sep.join( os.path.abspath(__file__).split(os.sep)[:-2])

BASE_INFO = {}
import getpass
ACT_USER = getpass.getuser()
# some formatting colors
class bcolors:
    """
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BASEINFO_CHANGED = """
%s--------------------------------------------------
The structure of the config files have changed.
You will be asked to provide some config data again.
--------------------------------------------------%s
""" %(bcolors.FAIL, bcolors.ENDC)

# base defaults are the defaults we are using for the base info if they where not set
user_home = os.path.expanduser('~')
BASE_DEFAULTS = {
    #name, explanation, default
    'sitesinfo_path' : (
        'sitesinfo path',                 # display
        'path to the folder where sites.py and sites_local.py is found\nThis folder should be maintained by git',    # help
        '%s/sites_list/' % BB_HOME  # default
    ),
    'sitesinfo_url' : (
        'sitesinfo url',                 # display
        'url to the repository where sites.py and sites_local.py is maintained.\nIf it is localhost it will be created for you but not added to a repo',    # help
        'https://gitlab.redcor.ch/redcor_customers/sites_list.git'   # default
    ),
    'project_path' : (
        'project path',                 # display
        'path to the projects\nHere a structure for each odoo site is created to build and run odoo servers',         # help
        '%s/projects' % user_home  # default
    ),
    'odoo_server_data_path' : (
        'server data path',              # display
        'path to server data. Here for every site a set of folders is created\nthat will contain the servers config filestore, log- and dump-files.',          # help
        '%s/odoo_instances' % user_home  # default
    ),
    #'docker_path_map' : (
        #'docker path map. use , to separate parts',              # display
        #'docker volume mappings when docker is run locally.', # help
        #ACT_USER == 'root' and () or ('%s/' % user_home, '/root/')
    #),
    'docker_dumper_image' : (
        'Image to be used to create a dumper container',              # display
        'When transfering data between sites we need a helper docker container that can access the database and dump the data into a file', # help
        'robertredcor/dumper',
    ),
    'repo_mapper' : (
        'Access Urls to the source code repositories',              # display
        'What is the urls to use when accesing github or gitlab.\n'\
        'provide a comma separated list of repository=url pairs\n'\
        'default "gitlab.redcor.ch=ssh://git@gitlab.redcor.ch:10022/"',
        'gitlab.redcor.ch=ssh://git@gitlab.redcor.ch:10022/',
    ),
    'local_user_mail' : (
        'mail address of the local user',              # display
        'mail address of the local user', # help
        '%s@redo2oo.ch' % ACT_USER,
    )
}
try:
    from base_info import base_info as BASE_INFO
    NEED_BASEINFO = False
    # check whether BASE_DEFAULTS has new keys
    for k in BASE_DEFAULTS.keys():
        if not BASE_INFO.has_key(k):
            NEED_BASEINFO = True
            print( BASEINFO_CHANGED)
except ImportError:
    NEED_BASEINFO = True
# what folders do we need to create in odoo_sites for a new site
FOLDERNAMES = ['addons','dump','etc','filestore', 'log', 'ssl']
# base info filename points to file where some default values are stored
# base_info = {'project_path': '/home/robert/projects', 'skeleton': 'odoo/skeleton'}
BASE_INFO_NAME = 'base_info'
BASE_INFO_FILENAME = '%s/config/%s.py' % (BB_HOME, BASE_INFO_NAME)

PROJECT_DEFAULTS = {
    #name, explanation, default
    'projectname' : ('project name', 'what is the project name', 'projectname'),
    'odoo_version' : ('odoo version', 'version of odoo', '9.0'),
}
# sites is a combination created from "regular" sites listed in sites.py
# an a list of localsites listed in local_sites.py
#from sites import SITES, SITES_L as SITES_LOCAL
# start with checking whether installation is finished
try:
    pwd = os.getcwd()
    from scripts.sites_handler import SitesHandler
    sites_handler = SitesHandler(BB_HOME) # will exit when installation not yet finished
    SITES, SITES_LOCAL = sites_handler.get_sites()
    # MARKER is used to mark the position in sites.py to add a new site description
    MARKER = sites_handler.marker # from messages.py
    try:
        from localdata import REMOTE_USER_DIC, APACHE_PATH, DB_USER, DB_PASSWORD
    except ImportError:
        print( 'please create config/localdata.py')
        print( 'it must have values for REMOTE_USER_DIC, APACHE_PATH, DB_USER, DB_PASSWORD, DB_PASSWORD_LOCAL')
        print( 'use template/localdata.py as template')
        sys.exit()
    except SyntaxError:
        print( 'please edit config/localdata.py')
    os.chdir(pwd)
except ImportError:
    APACHE_PATH = ''
    SITES, SITES_LOCAL = {},{}
    MARKER = ''
    sites_handler = None
except OSError:
    # we probably runing from within docker
    print( '-------------------------------------->>>>', os.getcwd())
    BASE_INFO['odoo_server_data_path'] = '/mnt/sites'
    if os.getcwd() == '/mnt/sites':
        print( '------------------------------')
        raise ImportError()
    
# try to get also NGINX_PATH
# if not possible, provide warning and assume standard location
try:
    from localdata import NGINX_PATH
except ImportError:
    print( bcolors.WARNING + '*' * 80)
    print( 'could not read nginx path from config.localdata')
    print( 'assuming it is: /etc/nginx/')
    print( 'you can fix this by executing: bin/e')
    print( "and adding: NGINX_PATH = '/etc/nginx/'")
    print( '*' * 80 + bcolors.ENDC)
    NGINX_PATH = '/etc/nginx/'
    
try:
    from localdata import DB_PASSWORD_LOCAL
except ImportError:
    # BBB
    DB_PASSWORD_LOCAL = 'admin'

if sites_handler:
    # automatically update sites list only, when BASE_INFO[''] is set
    sites_handler.pull()

# file to which site configuration will be written
LOGIN_INFO_FILE_TEMPLATE = '%s/login_info.cfg.in'

# file to which pip requirements will be written
REQUIREMENTS_FILE_TEMPLATE = '%s/install/requirements.txt'

SITES_HOME =  os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

try:
    from version_info import *
except:
    version_info = None
    
p =  os.path.split(os.path.realpath(__file__))[0]
if not os.path.exists('%s/globaldefaults.py' % p):
    ## silently copy the defualts file
    #act = os.getcwd()
    #os.chdir(p)
    open('%s/globaldefaults.py' % p, 'w').write(open('%s/../templates/globaldefaults.py' % p, 'r').read())
    #os.chdir(act)
from globaldefaults import GLOBALDEFAULTS

# NEED_NAME is a list of options that must provide a name
NEED_NAME = [
    "add_apache",
    "add_site",
    "add_site_local",
    "create",
    "create_certificate",
    "create_container",
    'copy_admin_pw',
    "dataupdate",
    "dataupdate_close_connections",
    "directories",
    "docker_add_ssh",
    #"docker_show",
    "edit_site",
    "module_add",
    "module_update",
    "modules_update",
    "name",
    "norefresh",
    'full_update',
    'full_update_rebuild',
    'full_update_rebuild_refresh',
    'update_install_serversetting',
]

# NO_NEED_NAME is a list of options that do not need to provide a name
NO_NEED_NAME = [
    "add_server",
    "alias",
    "docker_create_db_container",
    "edit_server",
    "list_sites",
    "listmodules",
    "module_create",
    "pull",
    "reset",
    "set_config",
    "shell",
    "show",
    "use_branch",
]
# need name and target 
NEED_TARGET = [
    'copy_admin_pw',
]
# is know IP to remote server needed
NO_NEED_SERVER_IP = [
    'edit_site',
]
ODOO_VERSIONS = {
    '9.0' : {
        'python_ver' : 'python2', 
        'python_path' : '/usr/bin/python2',
        'buildout_recipe_link' : "git+https://github.com/anybox/anybox.recipe.odoo#egg=a.r.odoo",
    }, 
    '10.0' : {
        'python_ver' : 'python2', 
        'python_path' : '/usr/bin/python2',
        'buildout_recipe_link' : "git+https://github.com/anybox/anybox.recipe.odoo#egg=a.r.odoo",
    },
    '11.0' : {
        'python_ver' : 'python3', 
        'python_path' : '/usr/bin/python3',
        'buildout_recipe_link' : "git+https://github.com/anybox/anybox.recipe.odoo#egg=a.r.odoo",
    }
}
FLECTRA_VERSIONS = {
}
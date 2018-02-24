# bridge-builder
Bridgebuilder does provide a set of tools to create oddo, flectra, cubicerp and similar odoo based erp systems

it is based on a tool that has been developed for internal use  
during the last couple of years  
[odoo_instances](https://gitlab.redcor.ch/open-source/odoo_instances)  
[odoo_instances/installation](https://gitlab.redcor.ch/open-source/odoo_instances/blob/master/install/INSTALL.txt)

odoo_instances is used to create local and remote odoo sites, create adn update docker_instances with running mirror of the local sites, doing ackups and a number of other dayly chores.

Its main features will be reimplemented in bridge-builder such that we can create functionally identical sites in any of the suported erp systems.

# Fetures ( as now implemedet in odoo_instances)
- Create sites from well structured description files  
  These description files define:
  - Base tools to install (like CRM)
  - What addons to install from where
  - What configuration settings to create
  - What mail-servers to install
  - Users to create and their mailsettings
- Automatic Nginx/Apache configuration
- Installation of lets-encript certification
- Creation of local sites running in a virtual env
- Creation of remote servers identical to the local ones runnin in a docker container
- fetching life live servers to a local box and vice versa
- maintaining docker images with all required libraries as needed for the divers instances
- supporting developement of own modules
- backup and restore of life servers
- ..




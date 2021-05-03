# First Install

  Pour ENV=production et ENV=staging:
  En tant que user Billing Account OVH:
    Créer un projet public cloud <APP_NAME>-nlpdata-<ENV>
    Transférer les droits Admin et Technical au Infra Account OVH.
  En tant que user Infra Account OVH:  
    Créer un utilisateur Openstack (Public Cloud > Users & Roles > Create User)
    Télécharger le fichier openrc.sh de ce user
    Prendre les lignes de ce fichier pour en faire des variables dans .env.ovh.<env>
    ajouter aussi dedans le OS_PASSWORD de votre user openstack
    Créer une instance public cloud c2-7 sgb5
    Créer un block storage
    Attacher le block storage à l'instance
  En tant que Billing Account OVH:
    Ajouter dans le domain <APP_NAME>.<TLD> le dns nlpdata.<APP_NAME>.<TLD> ou (nlpdata-staging.<APP_NAME>.<TLD>) associé à l'ip adresse de l'instance
  En local:
  ```
    ./<COMMAND_NAME> -e <ENV> -p nlpdata install
    ./<COMMAND_NAME> -e <ENV> -p nlpdata bash
  ```
  Dans le ssh du server, faire un screen:
  ```
    screen
  ```
  Dedans:
  ```
    sudo bash scripts/start_serve-ssl.sh
  ```

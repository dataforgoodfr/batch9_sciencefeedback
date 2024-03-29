# batch9_sciencefeedback

batch9_sciencefeedback is a microservice helping to retrieve expert scientists per domain.


## API


### /scientists

```bash
curl -X https://nlp.feedback.org/scientists?q=covid
```
returns 
```json
 [
   {
     "id": 1,
     "firstName": "Michel",
     "lastName": "Guillemin"
   },
   {
     "id": 2,
     "firstName": "Valentine",
     "lastName": "Rebeco"
   } 
 ]
```


### /hotclaims

```bash
curl -X https://nlp.feedback.org/hotclaims?date=05-05-2021
```
returns 
```json
 [
   {
     "id": 1,
     "text": "There is no climate emergency; Ecosystems are thriving and humanity is benefiting from increased carbon dioxide.",
   },
   {
     "id": 2, 
     "text": "Plugging this device into a car’s fuse box can reduce fuel consumption by at least 35% and up to 75% by converting the car into a hybrid."
   } 
 ]
```


## Webapp

Visit https://nlp.feedback.org/web

## Contributing


### Requirements
  - docker (https://docs.docker.com/install/)
  - docker-compose (https://docs.docker.com/compose/install/#install-compose)
  - coreutils (for macosx, via brew)


### Run
  ```bash
  ./b9sf start
  ```

### Deploy
  Check if the repo is updated with the last **master**. Then:
  ```bash
  ./b9sf -t I.P.S. tag
  ```

  If you are admin, you can deploy a specific tag to the production branch:
  ```bash
  ./b9sf -e production -t 3.0.1 deploy
  ```

### Commands
  Several commands are available in api/commands to run some scripts, for e.g. :
  ```bash
  ./bs9f torchserve 'my cat is a foo'
  ```
  returns the embed bert version of the query



### Datascience
  When serve-development is running, you have a jupyter notebook playground at localhost/jupyter
  helping you to import api functions and also play with your favorite libs in order
  to test your datascience proof of concept.

  Look at the .env/JUPYTER_TOKEN variable to see what is the token to enter on the notebook signin.

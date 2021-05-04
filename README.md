# batch9_sciencefeedback

## Requirements
  docker (https://docs.docker.com/install/)
  docker-compose (https://docs.docker.com/compose/install/#install-compose)
  coreutils (for macosx, via brew)


## Run
  ```bash
  ./b9sf start
  ```

## Deploy
  Check if the repo is updated with the last **master**. Then:
  ```bash
  ./b9sf -t I.P.S. tag
  ```

  Do a `git tag` if you want to know the current tag. After having checked that the ci worked, as an example:
  ```bash
  ./b9sf -e production -t 3.0.1 deploy
  ```
`

## Commands
  Several commands are available in api/commands to run some scripts, for e.g. :
  ```bash
  ./fb humanize 2
  ```
  returns the humanized version of the id 2

  If you want to make it running on a certain env:
  ```bash
  ./fb -e staging filter -n user -i1 email,foo@bar.com
  ```
  returns the user in the staging database having the foo@bar.com mail.


## Datascience
  When serve-development is running, you have a jupyter notebook playground at localhost/jupyter
  helping you to import api functions and also play with your favorite libs in order
  to test your datascience proof of concept.

  Look at the .env/JUPYTER_TOKEN variable to see what is the token to enter on the notebook signin.

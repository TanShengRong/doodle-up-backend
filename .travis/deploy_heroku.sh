#!/bin/sh
if [ $TRAVIS_BRANCH != "master" ] && [ $TRAVIS_PULL_REQUEST = "false" ]
then
  echo "we're not on master branch"
  exit 0
else
  wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
  heroku plugins:install @heroku-cli/plugin-container-registry
  docker login --username _ --password=$HEROKU_API_KEY registry.heroku.com
  heroku container:push web --app doodle-up-backend
  heroku container:release web --app doodle-up-backend
fi
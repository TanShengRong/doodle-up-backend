#!/bin/sh
# Pull requests shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo "Should not deploy pull request; just doing a build."
    exit 0
fi
if [ "$TRAVIS_BRANCH" != "master" ]; then
    echo "Should not deploy pull request; just doing a build."
    exit 0
fi
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
heroku plugins:install @heroku-cli/plugin-container-registry
docker login --username _ --password=$HEROKU_API_KEY registry.heroku.com
heroku container:push web --app doodle-up-backend
heroku container:release web --app doodle-up-backend
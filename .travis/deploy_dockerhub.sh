#!/bin/sh
if [ "$TRAVIS_BRANCH" != "master" ] && [ $TRAVIS_PULL_REQUEST = "false" ]
then
  echo "we're not on master branch"
  exit 0
else
  docker login --username $DOCKER_USER --password $DOCKER_PASS
  docker build -f Dockerfile -t $DOCKER_TAGN .
  docker tag $DOCKER_TAGN:latest $DOCKER_USER/$DOCKER_REPO:$DOCKER_TAGN
  docker push $DOCKER_USER/$DOCKER_REPO:$DOCKER_TAGN
fi

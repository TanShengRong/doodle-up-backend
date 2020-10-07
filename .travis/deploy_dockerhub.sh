docker login --username $DOCKER_USER --password $DOCKER_PASS
# if [ "$TRAVIS_BRANCH" = "master" ]; then
# TAG="latest"
# else
# TAG="$TRAVIS_BRANCH"
# fi
docker build -f Dockerfile -t doodle-up-backend .
docker tag doodle-up-backend:latest $DOCKER_USER/dockerhub:doodle-up-backend
# docker push $DOCKER_USER/dockerhub:$LOWERCASE_REPO_SLUG
docker push tansr77/dockerhub:doodle-up-backend
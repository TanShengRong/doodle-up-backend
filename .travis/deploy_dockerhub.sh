docker login --username $DOCKER_USER --password $DOCKER_PASS
# if [ "$TRAVIS_BRANCH" = "master" ]; then
# TAG="latest"
# else
# TAG="$TRAVIS_BRANCH"
# fi
docker build -f Dockerfile -t $LOWERCASE_REPO_SLUG:latest .
docker tag $LOWERCASE_REPO_SLUG:latest $DOCKER_USER/dockerhub:$LOWERCASE_REPO_SLUG
docker push $DOCKER_USER/dockerhub:$LOWERCASE_REPO_SLUG
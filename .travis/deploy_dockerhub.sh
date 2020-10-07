docker login --username $DOCKER_USER --password $DOCKER_PASS
if [ "$TRAVIS_BRANCH" = "master" ]; then
TAG="latest"
else
TAG="$TRAVIS_BRANCH"
fi
docker build -f Dockerfile -t $TRAVIS_REPO_SLUG:$TAG .
travis_repo_slug =`echo "$TRAVIS_REPO_SLUG" | tr '[:upper:]' '[:lower:]'` 
docker tag $travis_repo_slug $DOCKER_REPO
docker push $DOCKER_REPO
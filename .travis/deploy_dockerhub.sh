docker login --username $DOCKER_USER --password $DOCKER_PASS
docker build -f Dockerfile -t $DOCKER_TAGN .
docker tag $DOCKER_TAGN:latest $DOCKER_USER/$DOCKER_REPO:$DOCKER_TAGN
docker push $DOCKER_USER/$DOCKER_REPO:$DOCKER_TAGN
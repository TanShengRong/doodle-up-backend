wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
heroku plugins:install @heroku-cli/plugin-container-registry
docker login --username _ --password=$HEROKU_API_KEY registry.heroku.com
heroku container:push web --app serene-wildwood-43450
heroku container:release web --app serene-wildwood-43450
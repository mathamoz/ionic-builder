# Params are build id, github username, github reponame
echo "$(date): Creating container and starting build..."
JOB=$(docker run -d ionic-build /bin/bash -c "sh build.sh $1 $2 $3")
docker wait $JOB
echo "$(date): Copying build artifact from container..."
docker cp $JOB:/root/$2-$3.tar.gz .
echo "$(date): Removing container with ID $JOB..."
docker rm $JOB

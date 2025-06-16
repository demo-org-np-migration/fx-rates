#!/usr/bin/env bash
set -e

NS=$1
TAG=$(git rev-parse --short HEAD)

docker build -t ghcr.io/demo-org-np-migration/fx-rates:$TAG .
docker push ghcr.io/demo-org-np-migration/fx-rates:$TAG

sed -e "s/IMAGE_TAG/$TAG/" -e "s/ENV_PLACEHOLDER/$NS/" k8s/cronjob.yaml | kubectl apply -n $NS -f -

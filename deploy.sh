#!/usr/bin/env bash
set -e

NS=$1
TAG=$(git rev-parse --short HEAD)

# La imagen sha-$TAG la construye y la sube el workflow build (.github/workflows/build.yml) en cada push a main.

sed -e "s/IMAGE_TAG/$TAG/" -e "s/ENV_PLACEHOLDER/$NS/" k8s/cronjob.yaml | kubectl apply -n $NS -f -

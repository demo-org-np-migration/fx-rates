#!/usr/bin/env bash
set -e

NS=$1
TAG=sha-$(git rev-parse --short HEAD)

# La imagen $TAG la construye y la sube el workflow build (.github/workflows/build.yml) en cada push a main.

# La configuración del entorno primero (k8s/config-$NS.env -> ConfigMap fx-rates-config), después el CronJob.
kubectl create configmap fx-rates-config -n $NS --from-env-file="k8s/config-$NS.env" --dry-run=client -o yaml | kubectl apply -n $NS -f -
sed -e "s/IMAGE_TAG/$TAG/" -e "s/ENV_PLACEHOLDER/$NS/" k8s/cronjob.yaml | kubectl apply -n $NS -f -

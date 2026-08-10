#!/bin/bash -ex

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

IMAGE_NAME="${IMAGE_NAME:-example-python-flask}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
NAMESPACE="${NAMESPACE:-$(oc project -q)}"
REGISTRY="${REGISTRY:-image-registry.openshift-image-registry.svc:5000}"
FULL_IMAGE="${FULL_IMAGE:-${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}}"

if ! oc get imagestream "${IMAGE_NAME}" >/dev/null 2>&1; then
  oc create imagestream "${IMAGE_NAME}"
fi

oc registry login || podman login \
  -u "$(oc whoami)" \
  -p "$(oc whoami -t)" \
  "${REGISTRY}"

podman push "${FULL_IMAGE}"
echo "Pushed ${FULL_IMAGE}"

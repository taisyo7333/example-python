#!/bin/bash -ex

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

IMAGE_NAME="${IMAGE_NAME:-example-python-flask}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
NAMESPACE="${NAMESPACE:-$(oc project -q)}"
REGISTRY="${REGISTRY:-image-registry.openshift-image-registry.svc:5000}"
FULL_IMAGE="${FULL_IMAGE:-${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}}"

# Dev Spaces / restricted UIDs cannot write /run/containers; point auth at $HOME.
AUTH_FILE="${REGISTRY_AUTH_FILE:-$HOME/.config/containers/auth.json}"
mkdir -p "$(dirname "$AUTH_FILE")"
export REGISTRY_AUTH_FILE="$AUTH_FILE"

if ! oc get imagestream "${IMAGE_NAME}" >/dev/null 2>&1; then
  oc create imagestream "${IMAGE_NAME}"
fi

# Internal registry uses the cluster service CA, which is not in the default trust store.
oc registry login --to "$AUTH_FILE" --insecure \
  || podman login --tls-verify=false \
    -u "$(oc whoami)" \
    -p "$(oc whoami -t)" \
    "${REGISTRY}"

podman push --tls-verify=false "${FULL_IMAGE}"
echo "Pushed ${FULL_IMAGE}"

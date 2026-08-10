#!/bin/bash -ex

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

IMAGE_NAME="${IMAGE_NAME:-example-python-flask}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
NAMESPACE="${NAMESPACE:-$(oc project -q)}"
REGISTRY="${REGISTRY:-image-registry.openshift-image-registry.svc:5000}"
FULL_IMAGE="${FULL_IMAGE:-${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}}"

podman build -t "${FULL_IMAGE}" -f Containerfile .
echo "Built ${FULL_IMAGE}"

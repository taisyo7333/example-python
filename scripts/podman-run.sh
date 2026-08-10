#!/bin/bash -ex

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

IMAGE_NAME="${IMAGE_NAME:-example-python-flask}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
NAMESPACE="${NAMESPACE:-$(oc project -q)}"
REGISTRY="${REGISTRY:-image-registry.openshift-image-registry.svc:5000}"
FULL_IMAGE="${FULL_IMAGE:-${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}}"
DATABASE_URL="${DATABASE_URL:-postgresql://app:app@localhost:5432/appdb}"
HOST_PORT="${HOST_PORT:-5000}"

podman run --rm \
  -p "${HOST_PORT}:5000" \
  -e "DATABASE_URL=${DATABASE_URL}" \
  -e "FLASK_DEBUG=${FLASK_DEBUG:-0}" \
  "${FULL_IMAGE}"

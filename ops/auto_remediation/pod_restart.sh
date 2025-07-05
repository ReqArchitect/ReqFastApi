#!/bin/bash
# Restart a pod by label
kubectl rollout restart deployment "$1"

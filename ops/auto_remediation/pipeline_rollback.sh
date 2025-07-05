#!/bin/bash
# Roll back to previous pipeline image
kubectl rollout undo deployment "$1"

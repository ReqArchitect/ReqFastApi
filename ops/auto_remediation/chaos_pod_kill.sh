#!/bin/bash
# Simulate pod kill for chaos testing
kubectl delete pod -l app="$1" --force --grace-period=0

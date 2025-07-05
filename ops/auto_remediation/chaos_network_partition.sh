#!/bin/bash
# Simulate network partition (requires chaos mesh or similar)
# Example: block egress from a pod
kubectl exec "$1" -- iptables -A OUTPUT -d $BLOCK_IP -j DROP

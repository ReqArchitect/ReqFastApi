# AST-driven docker-compose.yml patcher for env_file and DB_URL cleanup
# Usage: python update_compose_envfiles.py

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

TARGETS = [
    'auth_service',
    'usage_service',
    'billing_service',
    'invoice_service',
    'notification_service',
    'audit_log_service',
    'ai_modeling_service',
]

def patch_service(service, node):
    # Insert env_file before environment
    if 'environment' in node:
        # Remove DB_URL or DATABASE_URL from environment
        env = node['environment']
        if isinstance(env, list):
            node['environment'] = [e for e in env if not (str(e).startswith('DB_URL=') or str(e).startswith('DATABASE_URL='))]
        elif isinstance(env, dict):
            for k in list(env.keys()):
                if k in ('DB_URL', 'DATABASE_URL'):
                    del env[k]
        # Insert env_file if not present
        if 'env_file' not in node:
            envfile_path = f"services/{service}/.env"
            node.insert(list(node).index('environment'), 'env_file', [envfile_path])

def main():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    compose_path = 'docker-compose.yml'
    with open(compose_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f)
    for service in TARGETS:
        if service in data['services']:
            patch_service(service, data['services'][service])
    with open(compose_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    print('✅ docker-compose.yml updated: env_file injected and DB_URL removed for target services.')

if __name__ == '__main__':
    main()

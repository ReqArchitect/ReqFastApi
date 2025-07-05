import string
import yaml
import json

def parse_prompt(template_text: str, input_text: str) -> str:
    # Use Python string.Template for variable substitution
    tpl = string.Template(template_text)
    prompt = tpl.safe_substitute(input_text=input_text)
    return prompt

def validate_output_format(prompt: str, fmt: str = "json") -> bool:
    if fmt == "json":
        try:
            json.loads(prompt)
            return True
        except Exception:
            return False
    elif fmt == "yaml":
        try:
            yaml.safe_load(prompt)
            return True
        except Exception:
            return False
    elif fmt == "markdown":
        return prompt.strip().startswith("#") or prompt.strip() != ""
    return False

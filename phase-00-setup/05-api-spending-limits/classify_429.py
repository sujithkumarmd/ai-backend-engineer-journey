import json

SAMPLE_ERROR_BODIES = [
    '{"error": {"code": "rate_limit_exceeded", "message": "Rate limit reached for requests per minute"}}',
    '{"error": {"code": "insufficient_quota", "message": "You exceeded your current quota"}}',
    '{"error": {"code": "project_spend_limit_exceeded", "message": "Project spend limit reached"}}',
    '{"error": {"code": "organization_spend_limit_exceeded", "message": "Organization spend limit reached"}}',
]

RETRYABLE_CODES = {"rate_limit_exceeded"}

for body in SAMPLE_ERROR_BODIES:
    error = json.loads(body)["error"]
    code = error["code"]

    if code in RETRYABLE_CODES:
        action = "slow down, wait, then retry"
    else:
        action = "stop: retrying won't help, a human must act"

    print(f"429 {code:<35} → {action}")

# to run these, run 
# pytest test/test-validator.py

from guardrails import Guard
from validator import QuotesPrice

# We use 'refrain' as the validator's fail action,
#  so we expect failures to always result in a guarded output of None
# Learn more about corrective actions here:
#  https://www.guardrailsai.com/docs/concepts/output/#%EF%B8%8F-specifying-corrective-actions
"""Prepared Fireworks request adapter, not an enabled live integration.

Protocol: https://docs.fireworks.ai/structured-responses/structured-response-formatting
Model: https://fireworks.ai/models/fireworks/muse-spark-open
No credentials are loaded and no HTTP transport is provided here. Account consent,
applied credits, prepaid stop and disabled auto-reload require separate verification.
"""
import copy
import json
from .meta import MetaExtractor, SCHEMA
from .replay_response import validate_response

class FireworksExtractor(MetaExtractor):
    model = 'accounts/fireworks/models/muse-spark-open'
    endpoint = 'https://api.fireworks.ai/inference/v1/chat/completions'

    def request(self, body):
        request = super().request(body)
        request['messages'][0]['content'] += ' Return JSON matching this schema: ' + json.dumps(SCHEMA)
        request['max_tokens'] = 2048
        request['temperature'] = 0
        return request

    def extract(self, body):
        if self.transport is None:
            raise RuntimeError('Live inference locked: provider consent, credits and prepaid stop not verified')
        response = self.transport(self.endpoint, self.request(body))
        if not isinstance(response, dict) or response.get('model') != self.model:
            raise ValueError('Expected exact Fireworks Meta open-weight model identity')
        # The shared validator defaults to the direct Meta model. Its local validation
        # remains replay-only and never establishes that an injected transport is live.
        envelope = copy.deepcopy(response)
        del envelope['model']
        return validate_response(body, envelope)['claims']

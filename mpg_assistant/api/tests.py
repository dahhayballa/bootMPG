import os
import sys
import tempfile
import types
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase


class DotEnvParsingRegressionTest(SimpleTestCase):
    def test_load_dotenv_strips_quotes_and_spaces(self):
        from config import settings as settings_module

        os.environ.pop('TEST_ANTHROPIC_KEY', None)

        with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
            tmp.write('TEST_ANTHROPIC_KEY=   " sk-ant-test-key-123  "\n')
            tmp_path = Path(tmp.name)

        try:
            settings_module._load_dotenv(tmp_path)
            self.assertEqual(os.environ['TEST_ANTHROPIC_KEY'], 'sk-ant-test-key-123')
        finally:
            tmp_path.unlink(missing_ok=True)
            os.environ.pop('TEST_ANTHROPIC_KEY', None)


class LlmErrorNormalizationRegressionTest(SimpleTestCase):
    def test_call_llm_maps_anthropic_authentication_error_to_runtime_error(self):
        from ai.services import call_llm

        settings.MPG_ASSISTANT['ANTHROPIC_API_KEY'] = 'test-key'
        settings.MPG_ASSISTANT['LLM_MODEL'] = 'test-model'

        class AuthenticationError(Exception):
            pass

        class FakeMessages:
            def create(self, **kwargs):
                raise AuthenticationError('invalid x-api-key')

        class FakeClient:
            def __init__(self, api_key=None):
                self.messages = FakeMessages()

        fake_anthropic_module = types.SimpleNamespace(
            Anthropic=FakeClient,
            AuthenticationError=AuthenticationError,
            APIStatusError=Exception,
        )

        with patch.dict(sys.modules, {'anthropic': fake_anthropic_module}):
            with self.assertRaises(RuntimeError):
                call_llm('system', [], 'question')

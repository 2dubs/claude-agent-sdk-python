"""Tests for max_turns validation."""

from unittest.mock import AsyncMock

import pytest

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient
from claude_agent_sdk.types import _validate_max_turns


class TestValidateMaxTurns:
    @pytest.mark.parametrize("value", [None, 1, 5, 1000])
    def test_accepts_valid_values(self, value):
        _validate_max_turns(ClaudeAgentOptions(max_turns=value))

    @pytest.mark.parametrize("value", [0, -1, 2.5, "3"])
    def test_rejects_invalid_values(self, value):
        with pytest.raises(ValueError):
            _validate_max_turns(ClaudeAgentOptions(max_turns=value))


class TestConnectValidatesMaxTurns:
    @pytest.mark.anyio
    async def test_connect_rejects_zero_before_transport_connects(self):
        transport = AsyncMock()
        client = ClaudeSDKClient(ClaudeAgentOptions(max_turns=0), transport=transport)

        with pytest.raises(ValueError, match="max_turns"):
            await client.connect()

        transport.connect.assert_not_called()

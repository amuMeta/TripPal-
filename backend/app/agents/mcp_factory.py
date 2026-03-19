from __future__ import annotations

from functools import lru_cache
from typing import Any

from app.config import settings

try:
    from hello_agents import MCPTool
except ImportError:  # pragma: no cover - optional dependency at runtime
    MCPTool = None


class MCPFactory:
    def __init__(self) -> None:
        self._tool = None

    def get_tool(self) -> Any | None:
        if self._tool is not None:
            return self._tool

        if MCPTool is None or not settings.amap_api_key:
            return None

        tool = MCPTool(
            server_type="nodejs",
            package_name="@sugarforever/amap-mcp-server",
            auto_expand=True,
        )
        tool.set_env({"AMAP_API_KEY": settings.amap_api_key})
        self._tool = tool
        return self._tool

    def call(self, name: str, payload: dict[str, Any]) -> Any | None:
        tool = self.get_tool()
        if tool is None:
            return None
        return tool.call(name, payload)


@lru_cache(maxsize=1)
def get_mcp_factory() -> MCPFactory:
    return MCPFactory()

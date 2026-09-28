# === FILE HEADER ===
# Title: Roblox Open Cloud Client
# Path: tools/roblox_coc_sync/client.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Open Cloud Groups + public Users helpers.
# === END FILE HEADER ===

"""Minimal Roblox Open Cloud Groups Read client (API key auth; no cookies)."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import requests

logger = logging.getLogger("cia.roblox_coc_sync.client")

OPEN_CLOUD_BASE = "https://apis.roblox.com/cloud/v2"
USERS_PUBLIC_BASE = "https://users.roblox.com/v1"


@dataclass(frozen=True, slots=True)
class GroupRole:
    """A Roblox group roleset."""

    role_id: str
    name: str
    rank: int
    member_count: int | None = None


@dataclass(frozen=True, slots=True)
class GroupMember:
    """A member in a group role."""

    user_id: str
    username: str


class RobloxRateLimitError(RuntimeError):
    """Raised when Open Cloud returns HTTP 429 after retries."""


class RobloxApiError(RuntimeError):
    """Raised for non-retryable Open Cloud / Users API failures."""


class RobloxOpenCloudClient:
    """Groups Read via ``x-api-key`` (user-owned key with ``group:read``)."""

    def __init__(
        self,
        api_key: str,
        *,
        session: requests.Session | None = None,
        timeout: float = 30.0,
        max_retries: int = 4,
    ) -> None:
        if not api_key.strip():
            raise ValueError("ROBLOX_OPEN_CLOUD_API_KEY is empty")
        self._api_key = api_key.strip()
        self._session = session or requests.Session()
        self._timeout = timeout
        self._max_retries = max_retries
        self._username_cache: dict[str, str] = {}
        self._roles_cache: dict[str, list[GroupRole]] = {}

    def list_roles(self, group_id: str) -> list[GroupRole]:
        """List roles for a group (cached per client instance)."""
        gid = str(group_id).strip()
        if gid in self._roles_cache:
            return self._roles_cache[gid]

        roles: list[GroupRole] = []
        page_token: str | None = None
        while True:
            params: dict[str, str | int] = {"maxPageSize": 100}
            if page_token:
                params["pageToken"] = page_token
            data = self._open_cloud_get(f"/groups/{gid}/roles", params=params)
            for item in data.get("groupRoles") or data.get("roles") or []:
                role_id = _role_id_from_path(item.get("id") or item.get("path") or "")
                rank_raw = item.get("rank", item.get("rankNumber", 0))
                roles.append(
                    GroupRole(
                        role_id=role_id,
                        name=str(item.get("displayName") or item.get("name") or ""),
                        rank=int(rank_raw),
                        member_count=_optional_int(item.get("memberCount")),
                    )
                )
            page_token = data.get("nextPageToken") or None
            if not page_token:
                break

        roles.sort(key=lambda r: r.rank, reverse=True)
        self._roles_cache[gid] = roles
        logger.info("event=list_roles group_id=%s count=%s", gid, len(roles))
        return roles

    def find_role_by_rank(self, group_id: str, rank: int) -> GroupRole | None:
        for role in self.list_roles(group_id):
            if role.rank == int(rank):
                return role
        return None

    def find_role_by_name(self, group_id: str, name: str) -> GroupRole | None:
        needle = name.strip().casefold()
        for role in self.list_roles(group_id):
            if role.name.casefold() == needle:
                return role
        return None

    def list_members_for_role(
        self,
        group_id: str,
        role: GroupRole,
        *,
        max_members: int = 25,
    ) -> list[GroupMember]:
        """List members in a roleset via filter=role=='groups/{id}/roles/{roleId}'."""
        gid = str(group_id).strip()
        role_path = f"groups/{gid}/roles/{role.role_id}"
        filter_expr = f"role=='{role_path}'"
        members: list[GroupMember] = []
        page_token: str | None = None

        while len(members) < max_members:
            params: dict[str, str | int] = {
                "maxPageSize": min(100, max_members - len(members)),
                "filter": filter_expr,
            }
            if page_token:
                params["pageToken"] = page_token
            data = self._open_cloud_get(f"/groups/{gid}/memberships", params=params)
            for item in data.get("groupMemberships") or []:
                user_path = str(item.get("user") or "")
                user_id = user_path.rsplit("/", 1)[-1] if user_path else ""
                if not user_id:
                    continue
                username = self.resolve_username(user_id)
                members.append(GroupMember(user_id=user_id, username=username))
                if len(members) >= max_members:
                    break
            page_token = data.get("nextPageToken") or None
            if not page_token:
                break

        logger.info(
            "event=list_members group_id=%s role_id=%s rank=%s count=%s",
            gid,
            role.role_id,
            role.rank,
            len(members),
        )
        return members

    def resolve_username(self, user_id: str) -> str:
        """Resolve Roblox username via public Users API (cached)."""
        uid = str(user_id).strip()
        if uid in self._username_cache:
            return self._username_cache[uid]
        url = f"{USERS_PUBLIC_BASE}/users/{uid}"
        response = self._request_with_retries("GET", url, headers={})
        data = response.json()
        name = str(data.get("name") or data.get("displayName") or uid)
        self._username_cache[uid] = name
        return name

    def _open_cloud_get(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{OPEN_CLOUD_BASE}{path}"
        headers = {"x-api-key": self._api_key, "Accept": "application/json"}
        # requests encodes filter; keep filter raw for Open Cloud (== and quotes).
        if params and "filter" in params:
            filter_value = quote(str(params["filter"]), safe="='/, ")
            other = {k: v for k, v in params.items() if k != "filter"}
            query = "&".join(
                [f"filter={filter_value}"]
                + [f"{k}={quote(str(v), safe='')}" for k, v in other.items()]
            )
            response = self._request_with_retries("GET", f"{url}?{query}", headers=headers)
        else:
            response = self._request_with_retries("GET", url, headers=headers, params=params)
        return response.json()

    def _request_with_retries(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        last_error: Exception | None = None
        for attempt in range(self._max_retries):
            try:
                response = self._session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    timeout=self._timeout,
                )
            except requests.RequestException as exc:
                last_error = exc
                sleep_s = min(2**attempt, 30)
                logger.warning(
                    "event=http_network_error attempt=%s sleep_s=%s error=%s",
                    attempt + 1,
                    sleep_s,
                    exc,
                )
                time.sleep(sleep_s)
                continue

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                sleep_s = (
                    float(retry_after)
                    if retry_after and retry_after.isdigit()
                    else min(2**attempt, 60)
                )
                logger.warning(
                    "event=rate_limited attempt=%s sleep_s=%s url=%s",
                    attempt + 1,
                    sleep_s,
                    url,
                )
                time.sleep(sleep_s)
                last_error = RobloxRateLimitError(f"429 from {url}")
                continue

            if response.status_code >= 400:
                raise RobloxApiError(
                    f"Roblox API {response.status_code} for {url}: {response.text[:400]}"
                )
            return response

        raise RobloxRateLimitError(f"Exhausted retries for {url}") from last_error


def _role_id_from_path(path: str) -> str:
    text = str(path).strip()
    if "/" in text:
        return text.rsplit("/", 1)[-1]
    return text


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/client.py
# Maintained by: docshamxo
# === END FILE FOOTER ===

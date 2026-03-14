from __future__ import annotations

ROLE_TIER_RANKS: dict[str, int] = {
    "SUPPORT": 10,
    "MODERATOR": 20,
    "OPERATOR": 20,
    "ADMIN": 30,
    "OWNER": 40,
}

LEGACY_ROLE_ALIASES: dict[str, str] = {
    "MODS": "MODERATOR",
    "OPS": "OPERATOR",
}


def canonicalize_role_code(role_code: str) -> str:
    normalized = role_code.strip().upper()
    return LEGACY_ROLE_ALIASES.get(normalized, normalized)


async def get_effective_tier(
    *,
    app_state: object,
    tenant_id: int,
    user_id: int,
    member_role_ids: set[int],
    owner_user_id: int,
) -> int:
    effective_rank = ROLE_TIER_RANKS["OWNER"] if user_id == owner_user_id else 0

    bindings = await app_state.repos.tenant_config_repo.list_role_bindings(tenant_id)
    for row in bindings:
        if int(row["platform_role_id"]) not in member_role_ids:
            continue
        code = canonicalize_role_code(str(row["code"]))
        rank = ROLE_TIER_RANKS.get(code)
        if rank is not None and rank > effective_rank:
            effective_rank = rank

    return effective_rank


async def require_min_role(
    *,
    app_state: object,
    tenant_id: int,
    user_id: int,
    owner_user_id: int,
    member_role_ids: set[int],
    minimum_role_code: str,
) -> bool:
    required_rank = ROLE_TIER_RANKS[canonicalize_role_code(minimum_role_code)]
    current_rank = await get_effective_tier(
        app_state=app_state,
        tenant_id=tenant_id,
        user_id=user_id,
        member_role_ids=member_role_ids,
        owner_user_id=owner_user_id,
    )
    return current_rank >= required_rank


async def require_runtime_writable(*, app_state: object, tenant_id: int, feature_name: str) -> bool:
    governance = await app_state.services.tenant_config_service.load_governance(tenant_id)
    if bool(governance.get("read_only_enabled")):
        return False

    flags = dict(governance.get("feature_flags", {}))
    return flags.get(feature_name, True)

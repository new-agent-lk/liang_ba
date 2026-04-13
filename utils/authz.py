from typing import Any

RESEARCHER_CATEGORY = "researcher"


def get_user_profile(user: Any):
    if not user or not getattr(user, "is_authenticated", False):
        return None
    return getattr(user, "profile", None)


def get_user_category(user: Any) -> str:
    profile = get_user_profile(user)
    return getattr(profile, "user_category", "") if profile else ""


def is_superuser_user(user: Any) -> bool:
    return bool(user and getattr(user, "is_authenticated", False) and user.is_superuser)


def is_manager_user(user: Any) -> bool:
    return bool(user and getattr(user, "is_authenticated", False) and user.is_staff)


def is_researcher_user(user: Any) -> bool:
    return bool(
        user
        and getattr(user, "is_authenticated", False)
        and get_user_category(user) == RESEARCHER_CATEGORY
    )


def can_access_console(user: Any) -> bool:
    return is_superuser_user(user) or is_manager_user(user) or is_researcher_user(user)


def get_console_role(user: Any) -> str:
    if is_superuser_user(user):
        return "superuser"
    if is_manager_user(user):
        return "manager"
    if is_researcher_user(user):
        return "researcher"
    return "user"


def get_console_capabilities(user: Any) -> list[str]:
    if not can_access_console(user):
        return []

    capabilities = {
        "console.access",
        "profile.manage",
        "reports.access",
        "reports.manage_own",
    }

    if is_manager_user(user):
        capabilities.update(
            {
                "dashboard.view",
                "system.users.manage",
                "system.settings.manage",
                "content.manage",
                "data.import_export.manage",
                "factorhub.manage",
                "logs.view",
                "reports.manage_all",
                "reports.review",
                "reports.publish",
                "reports.toggle_top",
            }
        )

    if is_superuser_user(user):
        capabilities.add("logs.manage")

    return sorted(capabilities)

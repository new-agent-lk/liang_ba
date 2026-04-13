import { ConsoleCapability, User } from "@/types";

type MenuItem = {
  key: string;
  label: string;
  icon?: string;
  requiredCapabilities?: ConsoleCapability[];
  children?: MenuItem[];
};

export const hasCapability = (
  user: User | null | undefined,
  capability: ConsoleCapability,
): boolean => {
  return Boolean(user?.capabilities?.includes(capability));
};

export const hasAnyCapability = (
  user: User | null | undefined,
  capabilities?: ConsoleCapability[],
): boolean => {
  if (!capabilities || capabilities.length === 0) {
    return true;
  }
  return capabilities.some((capability) => hasCapability(user, capability));
};

export const filterMenuItems = (
  items: MenuItem[],
  user: User | null | undefined,
): MenuItem[] => {
  return items
    .map((item) => {
      const children = item.children ? filterMenuItems(item.children, user) : [];
      const hasAccess = hasAnyCapability(user, item.requiredCapabilities);

      if (children.length > 0) {
        return { ...item, children };
      }

      if (!hasAccess) {
        return null;
      }

      return { ...item, children: undefined };
    })
    .filter((item): item is MenuItem => Boolean(item))
    .filter(
      (item) =>
        (item.children && item.children.length > 0) ||
        hasAnyCapability(user, item.requiredCapabilities),
    );
};

export const getDefaultRoute = (user: User | null | undefined): string => {
  if (hasCapability(user, "dashboard.view")) {
    return "/dashboard";
  }
  if (hasCapability(user, "reports.access")) {
    return "/research/reports";
  }
  if (hasCapability(user, "profile.manage")) {
    return "/system/profile";
  }
  return "/login";
};

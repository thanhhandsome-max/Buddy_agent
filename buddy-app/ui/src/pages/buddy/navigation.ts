import type { IconName } from "../../components/icon-data.ts";

export const BUDDY_NAVIGATION = {
  "buddy-coder": {
    title: "Buddy Coder",
    description: "OpenCode ngay trong Buddy",
    icon: "fileCode",
  },
  "buddy-security": {
    title: "Bảo mật",
    description: "Camera Safety và Cyber Security",
    icon: "shieldCheck",
  },
} as const satisfies Record<string, { title: string; description: string; icon: IconName }>;

export type BuddyRouteId = keyof typeof BUDDY_NAVIGATION;
export const BUDDY_ROUTES = ["buddy-coder", "buddy-security"] as const satisfies readonly BuddyRouteId[];

export function isBuddyRoute(id: string): id is BuddyRouteId {
  return Object.hasOwn(BUDDY_NAVIGATION, id);
}

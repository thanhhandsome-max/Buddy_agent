import {
  resolveThemeBranding,
  type ThemeBranding,
} from "../../../packages/gateway-protocol/src/theme.ts";
import { createChangeListeners } from "../../../src/shared/listeners.js";

export const BUDDY_BRAND_NAME = "Buddy";

export function resolveControlUiBranding(source: Parameters<typeof resolveThemeBranding>[0]) {
  const branding = resolveThemeBranding(source);
  return { ...branding, brandName: source?.brandName ?? BUDDY_BRAND_NAME };
}

let branding = resolveControlUiBranding(undefined);
const listeners = createChangeListeners();

export function setCurrentThemeBranding(value: ThemeBranding): void {
  branding = value;
  listeners.publish();
}

export function currentThemeBranding(): ThemeBranding {
  return branding;
}

/** Leaf elements outside the app context follow the same published theme. */
export function subscribeThemeBranding(listener: () => void): () => void {
  return listeners.subscribe(listener);
}

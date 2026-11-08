import { defineSolidPage } from "../../app-route-types.tsx";

export const pages = [
  defineSolidPage("buddy-coder", () => import("./buddy-page.tsx").then((module) => module.CoderPage)),
  defineSolidPage("buddy-security", () => import("./buddy-page.tsx").then((module) => module.SecurityPage)),
] as const;

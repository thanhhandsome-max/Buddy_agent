export type BuddyGatewayEvent = { event: string; payload?: unknown };

export type BuddyGatewayState = {
  scope: string;
  connected: boolean;
  sessionKey: string;
  agentId: string | null;
};

export interface BuddyGateway {
  snapshot(): BuddyGatewayState;
  subscribe(listener: () => void): () => void;
  subscribeEvents(listener: (event: BuddyGatewayEvent) => void): () => void;
  request<T = unknown>(method: string, params?: unknown): Promise<T>;
  href(path: string): string;
}

export function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

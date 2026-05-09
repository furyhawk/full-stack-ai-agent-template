import { registerOTel } from "@vercel/otel";

export function register() {
  registerOTel({
    serviceName: "ai_agent_4-frontend",
  });
}

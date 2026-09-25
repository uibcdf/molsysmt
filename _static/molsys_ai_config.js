// Default configuration for the MolSys-AI docs chat widget (pilot).
// You can override these values in the HTML pages (or another script) by
// assigning to `window.molsysAiChatConfig` before the widget script runs.

window.molsysAiChatConfig = window.molsysAiChatConfig || {
  // "placeholder": always show the friendly placeholder reply.
  // "backend": call the MolSys-AI chat API and show its responses.
  mode: "backend",
  // By default, talk to a chat API backend on the same origin.
  // If you serve docs under `uibcdf.org` and the API under `api.uibcdf.org`,
  // override this (or use the query-param toggles below).
  backendUrl: window.location.origin.replace(/\/+$/, "") + "/v1/chat",
  // Optional API key (only useful if the backend is configured to require it).
  // Note: if you set this in public docs pages, treat it as a public/low-privilege key.
  apiKey: "",
};

// Convenience toggles for local smoke tests (no rebuild required):
//
// - URL param:   ?molsys_ai_mode=backend
// - URL param:   ?molsys_ai_backend_url=http://127.0.0.1:8000/v1/chat
// - localStorage: localStorage.setItem("molsysAiChatMode", "backend")
//
// When serving docs and backend on different ports, you may need CORS on the
// backend (see `MOLSYS_AI_CORS_ORIGINS` in `server/chat_api/README.md`).
(function () {
  try {
    // If we are on the public docs domains, default to the public API domain.
    // This avoids requiring per-site config for `/molsysmt`, `/molsysviewer`, etc.
    // It also enables GitHub Pages previews (github.io) to talk to the API.
    if (
      window.location &&
      window.location.hostname &&
      (window.location.hostname.endsWith("uibcdf.org") ||
        window.location.hostname.endsWith("github.io"))
    ) {
      window.molsysAiChatConfig.backendUrl = "https://api.uibcdf.org/v1/chat";
    }

    const params = new URLSearchParams(window.location.search || "");
    const forcedMode =
      params.get("molsys_ai_mode") || window.localStorage.getItem("molsysAiChatMode");
    const forcedUrl =
      params.get("molsys_ai_backend_url") || window.localStorage.getItem("molsysAiChatBackendUrl");

    if (forcedMode) {
      window.molsysAiChatConfig.mode = forcedMode;
    }
    if (forcedUrl) {
      window.molsysAiChatConfig.backendUrl = forcedUrl;
    }
  } catch (e) {
    // Ignore configuration errors; keep defaults.
  }
})();

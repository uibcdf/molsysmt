
// Minimal MolSys-AI documentation chat widget (pilot).
//
// For the first pilot, the widget:
// - renders a small chat box on pages that include it,
// - captures user messages,
// - runs in "placeholder" mode (no network) or "backend" mode (calls `/v1/chat`).
//
// In backend mode, the widget sends full conversation history as `messages` and
// renders a compact “Sources” dropdown for each assistant reply.

(function () {
  function ensureString(value) {
    return typeof value === "string" ? value : "";
  }

  function asArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function ensureInt(value) {
    return typeof value === "number" && Number.isFinite(value) ? value : null;
  }

  function ensureUrl(value) {
    return typeof value === "string" && value.trim() ? value.trim() : null;
  }

  function ensurePath(value) {
    return typeof value === "string" && value.trim() ? value.trim() : null;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function highlightPython(code) {
    var tokenId = 0;
    var tokens = [];
    function protect(re, cls) {
      code = code.replace(re, function (match) {
        var token = "@@@TOK_" + tokenId + "@@@";
        tokens.push({ token: token, cls: cls, text: match });
        tokenId += 1;
        return token;
      });
    }

    protect(/("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')/g, "tok-string");
    protect(/#[^\n]*/g, "tok-comment");
    protect(/\b\d+(?:\.\d+)?\b/g, "tok-number");
    protect(
      /\b(as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|pass|raise|return|True|try|while|with|yield)\b/g,
      "tok-keyword"
    );

    var escaped = escapeHtml(code);
    tokens.forEach(function (tok) {
      var replacement = '<span class="' + tok.cls + '">' + escapeHtml(tok.text) + "</span>";
      escaped = escaped.split(tok.token).join(replacement);
    });
    return escaped;
  }

  function renderInline(text) {
    return escapeHtml(text).replace(/`([^`]+)`/g, function (_, code) {
      return "<code>" + escapeHtml(code) + "</code>";
    });
  }

  function renderMarkdownLite(text) {
    var lines = String(text || "").split(/\r?\n/);
    var out = [];
    var inCode = false;
    var codeLang = "";
    var codeLines = [];
    var paraLines = [];
    var listItems = [];

    function flushParagraph() {
      if (!paraLines.length) return;
      var paragraph = renderInline(paraLines.join(" ").trim());
      if (paragraph) {
        out.push("<p>" + paragraph + "</p>");
      }
      paraLines = [];
    }

    function flushList() {
      if (!listItems.length) return;
      var items = listItems.map(function (item) {
        return "<li>" + renderInline(item.trim()) + "</li>";
      });
      out.push("<ul>" + items.join("") + "</ul>");
      listItems = [];
    }

    function flushCode() {
      var raw = codeLines.join("\n");
      var lang = (codeLang || "").toLowerCase();
      var highlighted = lang === "python" || lang === "py" ? highlightPython(raw) : escapeHtml(raw);
      var className = lang ? "language-" + lang : "";
      out.push("<pre><code class=\"" + className + "\">" + highlighted + "</code></pre>");
      codeLines = [];
      codeLang = "";
    }

    lines.forEach(function (line) {
      var fence = line.match(/^```(\w+)?\s*$/);
      if (fence) {
        if (inCode) {
          flushCode();
          inCode = false;
        } else {
          flushParagraph();
          flushList();
          inCode = true;
          codeLang = fence[1] || "";
        }
        return;
      }

      if (inCode) {
        codeLines.push(line);
        return;
      }

      if (!line.trim()) {
        flushParagraph();
        flushList();
        return;
      }

      var listMatch = line.match(/^\s*[-*]\s+(.*)$/);
      if (listMatch) {
        flushParagraph();
        listItems.push(listMatch[1]);
        return;
      }

      flushList();
      paraLines.push(line.trim());
    });

    if (inCode) {
      flushCode();
    }
    flushParagraph();
    flushList();

    return out.join("\n");
  }

  function enhanceCodeBlocks(root) {
    if (!root) return;
    var blocks = root.querySelectorAll("pre > code");
    blocks.forEach(function (code) {
      var pre = code.parentElement;
      if (!pre) return;
      if (!pre.classList.contains("molsys-ai-code")) {
        pre.classList.add("molsys-ai-code");
      }

      if (!pre.querySelector(".molsys-ai-copy")) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "molsys-ai-copy";
        button.textContent = "Copy";
        button.addEventListener("click", function () {
          var text = code.textContent || "";
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function () {
              button.textContent = "Copied";
              setTimeout(function () {
                button.textContent = "Copy";
              }, 1500);
            });
          }
        });
        pre.appendChild(button);
      }
    });
  }

  function createChatContainer(root) {
    const globalConfig = window.molsysAiChatConfig || {};
    const mode = globalConfig.mode || "placeholder"; // "placeholder" | "backend"
    const apiKey = ensureString(globalConfig.apiKey || "");
    let backendUrl =
      globalConfig.backendUrl ||
      (window.location.origin.replace(/\/+$/, "") + "/v1/chat");
    const container = document.createElement("div");
    container.className = "molsys-ai-chat";
    container.style.border = "1px solid #ccc";
    container.style.borderRadius = "6px";
    container.style.maxWidth = "400px";
    container.style.height = "320px";
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.fontFamily = "system-ui, -apple-system, BlinkMacSystemFont, sans-serif";
    container.style.fontSize = "14px";
    container.style.backgroundColor = "#fafafa";

    const header = document.createElement("div");
    header.textContent = "MolSys-AI Docs Helper";
    header.style.padding = "8px 10px";
    header.style.borderBottom = "1px solid #ddd";
    header.style.fontWeight = "bold";
    header.style.backgroundColor = "#f0f0f0";

    const messages = document.createElement("div");
    messages.style.flex = "1";
    messages.style.padding = "8px";
    messages.style.overflowY = "auto";

    const inputRow = document.createElement("div");
    inputRow.style.display = "flex";
    inputRow.style.borderTop = "1px solid #ddd";

    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Ask something about the docs...";
    input.style.flex = "1";
    input.style.border = "none";
    input.style.padding = "8px";
    input.style.outline = "none";
    input.setAttribute("aria-label", "MolSys-AI docs chatbot input");

    const button = document.createElement("button");
    button.textContent = "Send";
    button.style.border = "none";
    button.style.padding = "0 12px";
    button.style.cursor = "pointer";
    button.style.backgroundColor = "#4a8af4";
    button.style.color = "#fff";
    button.style.fontWeight = "bold";

    inputRow.appendChild(input);
    inputRow.appendChild(button);

    container.appendChild(header);
    container.appendChild(messages);
    container.appendChild(inputRow);

    root.appendChild(container);

    function appendMessage(text, role, sources) {
      const wrapper = document.createElement("div");
      wrapper.style.display = "flex";
      wrapper.style.flexDirection = "column";
      wrapper.style.alignItems = role === "user" ? "flex-end" : "flex-start";

      const bubble = document.createElement("div");
      if (role === "assistant") {
        bubble.innerHTML = renderMarkdownLite(text || "");
        enhanceCodeBlocks(bubble);
      } else {
        bubble.textContent = text;
      }
      bubble.style.margin = "4px 0";
      bubble.style.padding = "6px 8px";
      bubble.style.borderRadius = "4px";
      bubble.style.maxWidth = "95%";

      if (role === "user") {
        bubble.style.backgroundColor = "#dbeafe";
      } else {
        bubble.style.backgroundColor = "#e5e7eb";
      }

      wrapper.appendChild(bubble);

      const srcs = asArray(sources);
      if (role === "assistant" && srcs.length) {
        const details = document.createElement("details");
        details.style.margin = "2px 0 6px 0";
        details.style.maxWidth = "95%";

        const summary = document.createElement("summary");
        summary.textContent = "Sources";
        summary.style.cursor = "pointer";
        summary.style.fontSize = "12px";
        summary.style.color = "#374151";
        details.appendChild(summary);

        const list = document.createElement("ol");
        list.style.margin = "6px 0 0 18px";
        list.style.padding = "0";
        list.style.fontSize = "12px";
        list.style.color = "#111827";

        srcs.forEach(function (s) {
          const li = document.createElement("li");
          const id = ensureInt(s && s.id);
          const url = ensureUrl(s && s.url);
          const path = ensurePath(s && s.path);

          const label = document.createElement("span");
          label.textContent = id ? "[" + id + "] " : "";
          li.appendChild(label);

          if (url) {
            const a = document.createElement("a");
            a.href = url;
            a.textContent = url;
            a.target = "_blank";
            a.rel = "noopener noreferrer";
            li.appendChild(a);
          } else if (path) {
            const code = document.createElement("code");
            code.textContent = path;
            li.appendChild(code);
          } else {
            li.textContent += "(unknown source)";
          }

          list.appendChild(li);
        });

        details.appendChild(list);
        wrapper.appendChild(details);
      }

      messages.appendChild(wrapper);
      messages.scrollTop = messages.scrollHeight;
    }

    const conversation = [];
    const greeting =
      mode === "backend"
        ? "Hi! Ask me about the MolSysSuite documentation."
        : "Hi! This MolSys-AI docs bot is not ready yet. Stay tuned for more features soon...";
    appendMessage(greeting, "assistant");
    conversation.push({ role: "assistant", content: greeting });

    function handleSend() {
      const text = input.value.trim();
      if (!text) return;
      appendMessage(text, "user");
      input.value = "";
      conversation.push({ role: "user", content: text });

      if (mode === "backend") {
        // Call the chat API backend. Even in backend mode this stays simple:
        // no streaming, just a single request/response.
        try {
          fetch(backendUrl, {
            method: "POST",
            headers: (function () {
              var headers = { "Content-Type": "application/json" };
              if (apiKey) {
                headers["Authorization"] = "Bearer " + apiKey;
              }
              return headers;
            })(),
            body: JSON.stringify({ messages: conversation, k: 5, client: "widget", rag: "on", sources: "on" }),
          })
            .then(function (resp) {
              if (!resp.ok) {
                throw new Error("HTTP " + resp.status);
              }
              return resp.json();
            })
            .then(function (data) {
              var answer = ensureString(data && (data.answer || data.content));
              if (!answer) {
                answer = "The docs backend did not return a valid answer.";
              }
              appendMessage(answer, "assistant", data && data.sources);
              conversation.push({ role: "assistant", content: answer });
            })
            .catch(function (err) {
              console.error("MolSys-AI docs widget error:", err);
              var fallback =
                "The docs backend is not available right now. "
                  + "Please try again later.";
              appendMessage(fallback, "assistant");
              conversation.push({ role: "assistant", content: fallback });
            });
        } catch (e) {
          console.error("MolSys-AI docs widget error:", e);
          var fallback =
            "The docs backend is not available right now. "
              + "Please try again later.";
          appendMessage(fallback, "assistant");
          conversation.push({ role: "assistant", content: fallback });
        }
      } else {
        // Placeholder mode: always respond with the same friendly message.
        var placeholder =
          "This bot is still under development. "
            + "In future versions it will answer questions about the MolSysSuite documentation.";
        appendMessage(placeholder, "assistant");
        conversation.push({ role: "assistant", content: placeholder });
      }
    }

    input.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") {
        ev.preventDefault();
        handleSend();
      }
    });
    button.addEventListener("click", handleSend);
  }

  function bootstrap() {
    var explicitRoot = document.getElementById("molsys-ai-chat");
    if (explicitRoot) {
      // Inline mode: render the chat box directly inside the given container.
      createChatContainer(explicitRoot);
    } else {
      // Fallback mode: create a floating launcher + panel in the bottom-right
      // corner of the page.
      var wrapper = document.createElement("div");
      wrapper.style.position = "fixed";
      wrapper.style.bottom = "16px";
      wrapper.style.right = "16px";
      wrapper.style.zIndex = "9999";
      wrapper.style.display = "flex";
      wrapper.style.flexDirection = "column";
      wrapper.style.alignItems = "flex-end";

      var panelHost = document.createElement("div");
      panelHost.style.marginBottom = "8px";
      panelHost.style.display = "none";

      createChatContainer(panelHost);

      var button = document.createElement("button");
      button.setAttribute("type", "button");
      button.setAttribute("aria-label", "Open MolSys-AI docs helper");
      button.textContent = "AI";
      button.style.width = "40px";
      button.style.height = "40px";
      button.style.borderRadius = "999px";
      button.style.border = "none";
      button.style.backgroundColor = "#4a8af4";
      button.style.color = "#fff";
      button.style.fontWeight = "bold";
      button.style.cursor = "pointer";
      button.style.boxShadow = "0 2px 6px rgba(0, 0, 0, 0.2)";

      var isOpen = false;
      function togglePanel() {
        isOpen = !isOpen;
        panelHost.style.display = isOpen ? "block" : "none";
        button.setAttribute(
          "aria-label",
          isOpen ? "Close MolSys-AI docs helper" : "Open MolSys-AI docs helper"
        );
      }

      button.addEventListener("click", togglePanel);

      wrapper.appendChild(panelHost);
      wrapper.appendChild(button);
      document.body.appendChild(wrapper);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootstrap);
  } else {
    bootstrap();
  }

  console.log("MolSys-AI docs widget loaded (pilot).");
})();

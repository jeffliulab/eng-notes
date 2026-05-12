(function () {
  var initialized = false;

  function replaceCodeBlocks(root) {
    var scope = root || document;
    scope.querySelectorAll("pre > code.language-mermaid").forEach(function (code) {
      var pre = code.parentElement;
      if (!pre || pre.getAttribute("data-mermaid-prepared") === "1") return;

      var block = document.createElement("div");
      block.className = "mermaid";
      block.textContent = code.textContent;
      pre.setAttribute("data-mermaid-prepared", "1");
      pre.replaceWith(block);
    });
  }

  function markProcessed(root) {
    (root || document).querySelectorAll(".mermaid").forEach(function (el) {
      el.setAttribute("data-mermaid-processed", "1");
    });
  }

  function render(root) {
    if (!window.mermaid) return;

    replaceCodeBlocks(root);

    if (!initialized) {
      window.mermaid.initialize({
        startOnLoad: false,
        securityLevel: "loose",
        theme: "default",
      });
      initialized = true;
    }

    if (typeof window.mermaid.run === "function") {
      window.mermaid.run({
        querySelector: ".mermaid:not([data-mermaid-processed='1'])",
      }).then(function () {
        markProcessed(root);
      });
      return;
    }

    if (typeof window.mermaid.init === "function") {
      var nodes = (root || document).querySelectorAll(".mermaid:not([data-mermaid-processed='1'])");
      if (nodes.length) {
        window.mermaid.init(undefined, nodes);
        markProcessed(root);
      }
    }
  }

  function boot() {
    render(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      window.requestAnimationFrame(function () {
        render(document);
      });
    });
  }
})();

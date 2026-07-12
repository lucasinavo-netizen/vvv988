(function () {
  if (window.__affiliateClickTrackingInstalled) return;
  window.__affiliateClickTrackingInstalled = true;

  function textOf(link) {
    return (link.textContent || "").replace(/\s+/g, " ").trim().slice(0, 120);
  }

  function getPlacement(link) {
    if (link.closest("header, nav")) return "nav";
    if (link.closest("footer")) return "footer";
    if (link.closest("article")) return "article_cta";
    var section = link.closest("[data-placement], [class], [id], section, main");
    var marker = [
      section && section.getAttribute("data-placement"),
      section && section.getAttribute("id"),
      section && section.getAttribute("class"),
      link.getAttribute("class")
    ].filter(Boolean).join(" ").toLowerCase();
    if (marker.indexOf("hero") !== -1) return "hero";
    if (marker.indexOf("card") !== -1 || marker.indexOf("grid") !== -1) return "card";
    if (marker.indexOf("cta") !== -1 || marker.indexOf("button") !== -1) return "cta";
    return "content";
  }

  document.addEventListener("click", function (event) {
    var link = event.target && event.target.closest ? event.target.closest("a[href]") : null;
    if (!link) return;

    var rawHref = link.getAttribute("href") || "";
    var url;
    try {
      url = new URL(rawHref, window.location.href);
    } catch (error) {
      return;
    }

    if (url.pathname.indexOf("/go/") !== 0) return;

    var payload = {
      event_category: "affiliate",
      event_label: url.pathname,
      go_path: url.pathname,
      link_url: url.href,
      link_text: textOf(link),
      page_location: window.location.href,
      page_path: window.location.pathname,
      site: window.location.hostname.replace(/^www\./, ""),
      placement: getPlacement(link),
      transport_type: "beacon"
    };

    if (typeof window.gtag === "function") {
      window.gtag("event", "affiliate_click", payload);
    }
  }, true);
})();

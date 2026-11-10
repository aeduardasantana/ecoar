/* ECOAR / GEB - GA4 apenas mediante consentimento. */
(function () {
  "use strict";
  var measurementId = "G-G4C7TJ2K13";
  var key = "ecoar_analytics_consent_v1";
  var preference = null;
  var loaded = false;
  try { preference = localStorage.getItem(key); } catch (e) {}

  function loadAnalytics() {
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", measurementId, { send_page_view: true });
    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(measurementId);
    document.head.appendChild(script);
  }

  function removePanel() {
    var existing = document.getElementById("ecoar-ga4-consent");
    if (existing) existing.remove();
  }

  function selectPreference(value) {
    var prior = preference;
    preference = value;
    try { localStorage.setItem(key, value); } catch (e) {}
    removePanel();
    if (value === "granted") loadAnalytics();
    else if (loaded && prior === "granted") window.location.reload();
  }

  function openPanel() {
    removePanel();
    var panel = document.createElement("section");
    panel.id = "ecoar-ga4-consent";
    panel.setAttribute("aria-label", "Preferências de privacidade e medição");
    panel.style.cssText = "position:fixed;bottom:16px;left:16px;right:16px;max-width:620px;margin:auto;z-index:2147483000;background:#fff;color:#14211b;border:1px solid #627065;box-shadow:0 8px 28px rgba(0,0,0,.24);padding:18px;font:14px/1.5 system-ui,Arial,sans-serif";
    var title = document.createElement("strong");
    title.textContent = "Privacidade e medição";
    title.style.cssText = "display:block;font-size:17px;margin-bottom:8px";
    var message = document.createElement("p");
    message.textContent = "Com sua autorização, o ECOAR utiliza o Google Analytics para compreender as visitas e melhorar a experiência do site. Você pode continuar sem medição e alterar sua escolha depois.";
    message.style.cssText = "margin:0 0 12px";
    var link = document.createElement("a");
    link.href = "https://gebempresarial.grupoeduardabispo.com.br/privacidade/";
    link.textContent = "Política de privacidade";
    link.style.cssText = "display:inline-block;margin-bottom:12px;color:#14211b;text-decoration:underline";
    var actions = document.createElement("div");
    actions.style.cssText = "display:flex;gap:8px;flex-wrap:wrap";
    [["Continuar sem medição", "denied"], ["Aceitar medição", "granted"]].forEach(function (option) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = option[0];
      b.style.cssText = "min-height:44px;padding:10px 14px;border:1px solid #14211b;cursor:pointer;font:600 13px system-ui,Arial,sans-serif;background:" + (option[1] === "granted" ? "#14211b" : "#fff") + ";color:" + (option[1] === "granted" ? "#fff" : "#14211b");
      b.addEventListener("click", function () { selectPreference(option[1]); });
      actions.appendChild(b);
    });
    panel.append(title, message, link, actions);
    document.body.appendChild(panel);
  }

  function init() {
    var button = document.createElement("button");
    button.type = "button";
    button.textContent = "Privacidade";
    button.setAttribute("aria-label", "Alterar preferências de medição");
    button.style.cssText = "position:fixed;bottom:8px;left:8px;min-height:36px;z-index:2147482999;background:#fff;color:#14211b;border:1px solid #627065;padding:7px 10px;cursor:pointer;font:12px system-ui,Arial,sans-serif";
    button.addEventListener("click", openPanel);
    document.body.appendChild(button);
    if (preference === "granted") loadAnalytics();
    else if (preference !== "denied") openPanel();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

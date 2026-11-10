/* 1st VRL Packers and Movers - site script. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");

  function closeNav() {
    if (!toggle || !nav) { return; }
    nav.classList.remove("nav--open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("nav--open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      if (open) {
        var first = nav.querySelector("a");
        if (first) { first.focus(); }
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("nav--open")) {
        closeNav();
        toggle.focus();
      }
    });

    document.addEventListener("click", function (e) {
      if (!nav.classList.contains("nav--open")) { return; }
      if (nav.contains(e.target) || toggle.contains(e.target)) { return; }
      closeNav();
    });
  }

  var yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  var status = document.querySelector("form.quote-form .form-status");

  function showStatus(msg, isError) {
    if (!status) { return; }
    status.textContent = msg;
    status.className = "form-status " + (isError ? "form-status--error" : "form-status--ok");
  }

  /* mail.php sends the visitor back to the same page with ?err=1 on a
     failed validation (empty name, short phone, or a filled honeypot). */
  if (status && /[?&]err=1/.test(window.location.search)) {
    showStatus("We could not send that. Check the phone number (10 digits) and send again, or call +91 82640 91243.", true);
    try { window.history.replaceState(null, "", window.location.pathname); } catch (e) {}
  }

  Array.prototype.forEach.call(document.querySelectorAll("form.quote-form"), function (form) {
    form.addEventListener("submit", function (e) {
      var name = form.querySelector('input[name="name"]');
      var phone = form.querySelector('input[name="phone"]');
      var digits = phone ? phone.value.replace(/[^0-9]/g, "") : "";

      if (!name || name.value.replace(/^\s+|\s+$/g, "").length < 2) {
        e.preventDefault();
        showStatus("Please enter your name so the coordinator knows who to ask for.", true);
        if (name) { name.focus(); }
        return;
      }
      if (digits.length < 10) {
        e.preventDefault();
        showStatus("Please enter a 10 digit phone number so the coordinator can call you back.", true);
        if (phone) { phone.focus(); }
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Sending\u2026";
      }
      showStatus("Sending your details\u2026", false);
    });
  });
})();

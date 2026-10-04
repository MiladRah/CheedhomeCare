// Cheed Home Care — small site script (menu, footer year, contact form)

// Mobile menu
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;
  toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.classList.contains("open")) {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    }
  });
})();

// Footer year
document.querySelectorAll("[data-year]").forEach(function (el) {
  el.textContent = new Date().getFullYear();
});

// Pre-select "I am interested in" from links like contact.html?interest=Companionship
(function () {
  var select = document.getElementById("interest");
  if (!select) return;
  var wanted = new URLSearchParams(window.location.search).get("interest");
  if (!wanted) return;
  for (var i = 0; i < select.options.length; i++) {
    if (select.options[i].value === wanted) { select.selectedIndex = i; break; }
  }
})();

// Contact form → Web3Forms (sends submissions to the business email; nothing is stored on this site)
(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  var button = form.querySelector("button[type=submit]");

  function show(kind, msg) {
    status.className = "form-status " + kind;
    status.textContent = msg;
    status.focus();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;

    var key = form.querySelector("[name=access_key]").value;
    if (!key || key.indexOf("YOUR_") === 0) {
      show("err", "The contact form isn't connected yet. Please call or text 587-973-0318, or email info@cheedinc.com.");
      return;
    }

    var data = Object.fromEntries(new FormData(form).entries());
    if (data.botcheck) return; // spam bot filled the hidden field
    data.subject = "New website enquiry from " + (data.first_name || "a visitor");

    button.disabled = true;
    var label = button.textContent;
    button.textContent = "Sending…";

    fetch(form.action, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.success) {
          form.reset();
          show("ok", "Thank you — your message was sent. We'll get back to you as soon as possible to set up your free consultation.");
        } else {
          throw new Error(res.message || "Send failed");
        }
      })
      .catch(function () {
        show("err", "Your message couldn't be sent. Please try again, or call or text us at 587-973-0318.");
      })
      .finally(function () {
        button.disabled = false;
        button.textContent = label;
      });
  });
})();

/* ACE Roofing — site scripts (no dependencies) */

/* --------------------------------------------------------------------------
   FORM SETUP
   Both forms (free inspection + contact page) are sent through Web3Forms
   (https://web3forms.com), which emails each request to the address the
   Web3Forms account that owns the access key below (aceco@aceroofingtx.com). The access key
   is not a secret; it only lets this site send to that inbox. Submissions
   are logged in the Web3Forms dashboard.
   -------------------------------------------------------------------------- */
const FORM_ENDPOINT = "https://api.web3forms.com/submit";
const FORM_ACCESS_KEY = "42dbcec6-908f-4823-b6cf-9a6bb407781d";

const PHONE_DISPLAY = "(956) 534-2911";

document.addEventListener("DOMContentLoaded", () => {
  /* Mobile navigation ---------------------------------------------------- */
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll(".has-dropdown > .nav__link[aria-haspopup]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const li = btn.parentElement;
      // On desktop the parent link navigates; on mobile it expands the submenu.
      if (window.matchMedia("(max-width: 960px)").matches) {
        e.preventDefault();
        const open = li.classList.toggle("open");
        btn.setAttribute("aria-expanded", String(open));
      }
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
      document.body.classList.remove("nav-open");
      toggle && toggle.setAttribute("aria-expanded", "false");
    }
  });

  /* Analytics events (Google Analytics 4) -------------------------------- */
  // Phone taps are the main way customers reach ACE Roofing, so count them.
  document.addEventListener("click", (e) => {
    const tel = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (tel && typeof window.gtag === "function") {
      window.gtag("event", "phone_call_click", {
        link_text: (tel.textContent || "").trim().slice(0, 60),
        page_path: window.location.pathname,
      });
    }
  });

  /* Footer year ---------------------------------------------------------- */
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  /* Gallery lightbox ----------------------------------------------------- */
  const links = Array.from(document.querySelectorAll("[data-lightbox]"));
  if (links.length) {
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Project photo");
    // Built with DOM methods (no innerHTML) so it works under Trusted Types.
    const button = (cls, label, text) => {
      const b = document.createElement("button");
      b.className = cls;
      b.setAttribute("aria-label", label);
      b.textContent = text;
      return b;
    };
    const img = document.createElement("img");
    img.alt = "";
    lb.append(
      button("lb-close", "Close", "×"),
      button("lb-prev", "Previous photo", "‹"),
      img,
      button("lb-next", "Next photo", "›")
    );
    document.body.appendChild(lb);
    let idx = 0;

    const show = (i) => {
      idx = (i + links.length) % links.length;
      img.src = links[idx].href;
      img.alt = links[idx].querySelector("img")?.alt || "";
    };
    const close = () => lb.classList.remove("open");

    links.forEach((a, i) =>
      a.addEventListener("click", (e) => {
        e.preventDefault();
        show(i);
        lb.classList.add("open");
        lb.querySelector(".lb-close").focus();
      })
    );
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", () => show(idx - 1));
    lb.querySelector(".lb-next").addEventListener("click", () => show(idx + 1));
    lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
    document.addEventListener("keydown", (e) => {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
  }

  /* Forms ---------------------------------------------------------------- */
  document.querySelectorAll("form[data-contact-form]").forEach((form) => {
    const status = form.querySelector(".form-status");
    const submit = form.querySelector("[type=submit]");

    const say = (msg, ok) => {
      status.textContent = msg;
      status.className = "form-status " + (ok ? "is-success" : "is-error");
    };

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;

      if (!FORM_ENDPOINT) {
        say(`Online requests aren't connected yet. Please call us at ${PHONE_DISPLAY} and we'll schedule your free inspection.`, false);
        return;
      }

      submit.disabled = true;
      const original = submit.textContent;
      submit.textContent = "Sending…";
      try {
        // Collect fields; checkboxes with the same name are joined with commas.
        const data = {};
        new FormData(form).forEach((value, key) => {
          data[key] = data[key] ? `${data[key]}, ${value}` : value;
        });
        if (data._honey) return; // spam bot filled the hidden field
        delete data._honey;
        data.access_key = FORM_ACCESS_KEY;
        data.subject = data._subject || "New website request — aceroofingtx.com";
        delete data._subject;
        data.from_name = "ACE Roofing website";
        if (data.email) data.replyto = data.email;
        data["Page"] = window.location.href;

        const res = await fetch(FORM_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(data),
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok || json.success !== true) throw new Error(json.message || String(res.status));
        form.reset();
        say("Thank you for contacting us. We will get back to you as soon as possible.", true);
        if (typeof window.gtag === "function") {
          window.gtag("event", "generate_lead", {
            form_name: form.querySelector("h2, h3")?.textContent.trim().slice(0, 60) || "contact",
            page_path: window.location.pathname,
          });
        }
      } catch (err) {
        say(`Oops, there was an error sending your message. Please try again, or call us at ${PHONE_DISPLAY}.`, false);
      } finally {
        submit.disabled = false;
        submit.textContent = original;
      }
    });
  });
});

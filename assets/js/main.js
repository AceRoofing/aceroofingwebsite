/* ACE Roofing — site scripts (no dependencies) */

/* --------------------------------------------------------------------------
   FORM SETUP
   The contact forms need a form service to deliver submissions by email.
   1. Create a free form at https://formspree.io (or a similar service).
   2. Paste the endpoint URL it gives you below, e.g.
      "https://formspree.io/f/abcdwxyz"
   Until this is set, the forms show a message asking visitors to call instead.
   -------------------------------------------------------------------------- */
const FORM_ENDPOINT = "";

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
    lb.innerHTML =
      '<button class="lb-close" aria-label="Close">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous photo">&#8249;</button>' +
      '<img alt="">' +
      '<button class="lb-next" aria-label="Next photo">&#8250;</button>';
    document.body.appendChild(lb);
    const img = lb.querySelector("img");
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
        const res = await fetch(FORM_ENDPOINT, {
          method: "POST",
          body: new FormData(form),
          headers: { Accept: "application/json" },
        });
        if (!res.ok) throw new Error(String(res.status));
        form.reset();
        say("Thank you for contacting us. We will get back to you as soon as possible.", true);
      } catch (err) {
        say(`Oops, there was an error sending your message. Please try again, or call us at ${PHONE_DISPLAY}.`, false);
      } finally {
        submit.disabled = false;
        submit.textContent = original;
      }
    });
  });
});

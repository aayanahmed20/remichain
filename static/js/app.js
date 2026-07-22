(function () {
    "use strict";

   var root = document.documentElement;
    var THEME_KEY = "remichain-theme";

   function applyTheme(theme) {
         root.setAttribute("data-theme", theme);
         var btn = document.getElementById("themeToggle");
         if (btn) {
                 btn.textContent = theme === "dark" ? "\u2600" : "\u{1F319}";
         }
   }

   function initTheme() {
         var saved = localStorage.getItem(THEME_KEY);
         var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
         applyTheme(saved || (prefersDark ? "dark" : "light"));

      var toggle = document.getElementById("themeToggle");
         if (toggle) {
                 toggle.addEventListener("click", function () {
                           var current = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
                           applyTheme(current);
                           localStorage.setItem(THEME_KEY, current);
                 });
         }
   }

   function initMobileNav() {
         var navToggle = document.getElementById("navToggle");
         var navLinks = document.getElementById("navLinks");
         if (!navToggle || !navLinks) return;
         navToggle.addEventListener("click", function () {
                 var isOpen = navLinks.classList.toggle("open");
                 navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
         });
   }

   function initFlashMessages() {
         var flashes = document.querySelectorAll(".flash");
         flashes.forEach(function (flash) {
                 var closeBtn = flash.querySelector(".flash-close");
                 if (closeBtn) {
                           closeBtn.addEventListener("click", function () {
                                       flash.style.display = "none";
                           });
                 }
                 setTimeout(function () {
                           flash.style.display = "none";
                 }, 8000);
         });
   }

   function initBackToTop() {
         var btn = document.getElementById("backToTop");
         if (!btn) return;
         window.addEventListener("scroll", function () {
                 if (window.scrollY > 400) {
                           btn.classList.add("visible");
                 } else {
                           btn.classList.remove("visible");
                 }
         });
         btn.addEventListener("click", function () {
                 window.scrollTo({ top: 0, behavior: "smooth" });
         });
   }

   function initCharCounters() {
         document.querySelectorAll("textarea[maxlength]").forEach(function (el) {
                 var counter = document.querySelector('.char-counter[data-for="' + el.id + '"]');
                 if (!counter) return;
                 var max = el.getAttribute("maxlength");
                 function update() {
                           var len = el.value.length;
                           counter.textContent = len + "/" + max;
                           counter.classList.toggle("limit-close", max - len < 20);
                 }
                 el.addEventListener("input", update);
                 update();
         });
   }

   function initFormSubmitState() {
         document.querySelectorAll("form.form-card").forEach(function (form) {
                 form.addEventListener("submit", function () {
                           var btn = form.querySelector('button[type="submit"]');
                           if (btn && !btn.disabled) {
                                       btn.dataset.originalText = btn.innerHTML;
                                       btn.innerHTML = '<span class="spinner"></span> Submitting\u2026';
                                       btn.disabled = true;
                           }
                 });
         });
   }

   function initTableSearch() {
         document.querySelectorAll(".table-search").forEach(function (input) {
                 var table = document.getElementById(input.dataset.target);
                 if (!table) return;
                 input.addEventListener("input", function () {
                           var q = input.value.trim().toLowerCase();
                           table.querySelectorAll("tbody tr").forEach(function (row) {
                                       var text = row.textContent.toLowerCase();
                                       row.classList.toggle("row-hidden", q.length > 0 && text.indexOf(q) === -1);
                           });
                 });
         });
   }

   function initSortableTables() {
         document.querySelectorAll("table[data-sortable]").forEach(function (table) {
                 var headers = table.querySelectorAll("th[data-sort]");
                 headers.forEach(function (th, index) {
                           th.addEventListener("click", function () {
                                       var type = th.getAttribute("data-sort");
                                       var tbody = table.querySelector("tbody");
                                       var rows = Array.prototype.slice.call(tbody.querySelectorAll("tr"));
                                       var asc = !th.classList.contains("sort-asc");

                                                         headers.forEach(function (h) {
                                                                       h.classList.remove("sort-asc", "sort-desc");
                                                         });
                                       th.classList.add(asc ? "sort-asc" : "sort-desc");

                                                         rows.sort(function (a, b) {
                                                                       var av = a.children[index].textContent.trim();
                                                                       var bv = b.children[index].textContent.trim();
                                                                       if (type === "number") {
                                                                                       av = parseFloat(av) || 0;
                                                                                       bv = parseFloat(bv) || 0;
                                                                                       return asc ? av - bv : bv - av;
                                                                       }
                                                                       return asc ? av.localeCompare(bv) : bv.localeCompare(av);
                                                         });

                                                         rows.forEach(function (row) {
                                                                       tbody.appendChild(row);
                                                         });
                           });
                 });
         });
   }

   function initExpiryWarnings() {
         var now = new Date();
         document.querySelectorAll("td[data-expiry]").forEach(function (cell) {
                 var value = cell.getAttribute("data-expiry");
                 if (!value) return;
                 var expiry = new Date(value);
                 if (isNaN(expiry.getTime())) return;
                 var days = (expiry - now) / (1000 * 60 * 60 * 24);
                 if (days < 0) return;
                 if (days <= 7) {
                           cell.classList.add("expiry-critical");
                 } else if (days <= 30) {
                           cell.classList.add("expiry-warning");
                 }
         });
   }

   function initFooterYear() {
         var el = document.getElementById("year");
         if (el) el.textContent = new Date().getFullYear();
   }

   function initActiveNav() {
         var links = document.querySelectorAll(".nav-links a");
         links.forEach(function (link) {
                 if (link.getAttribute("href") === window.location.pathname) {
                           link.classList.add("active");
                 }
         });
   }

   document.addEventListener("DOMContentLoaded", function () {
         initTheme();
         initMobileNav();
         initFlashMessages();
         initBackToTop();
         initCharCounters();
         initFormSubmitState();
         initTableSearch();
         initSortableTables();
         initExpiryWarnings();
         initFooterYear();
         initActiveNav();
   });
})();

document.addEventListener("DOMContentLoaded", () => {
  const toggler = document.querySelector("[data-sidebar-toggle]");
  const sidebar = document.querySelector("[data-sidebar]");
  if (toggler && sidebar) {
    toggler.addEventListener("click", () => {
      sidebar.classList.toggle("-translate-x-full");
    });
  }

  const userMenuButton = document.querySelector("[data-user-menu-button]");
  const userMenu = document.querySelector("[data-user-menu]");
  if (userMenuButton && userMenu) {
    userMenuButton.addEventListener("click", event => {
      event.stopPropagation();
      userMenu.classList.toggle("hidden");
    });

    document.addEventListener("click", () => {
      if (!userMenu.classList.contains("hidden")) {
        userMenu.classList.add("hidden");
      }
    });
  }

  document.querySelectorAll("[data-extend-wrapper]").forEach(wrapper => {
    const toggle = wrapper.querySelector("[data-extend-toggle]");
    const panel = wrapper.querySelector("[data-extend-panel]");
    const cancel = wrapper.querySelector("[data-extend-cancel]");
    if (!toggle || !panel) return;

    function closePanel() {
      panel.classList.add("hidden");
    }

    toggle.addEventListener("click", event => {
      event.stopPropagation();
      panel.classList.toggle("hidden");
    });

    if (cancel) {
      cancel.addEventListener("click", event => {
        event.preventDefault();
        closePanel();
      });
    }

    document.addEventListener("click", event => {
      if (panel.classList.contains("hidden")) return;
      if (!wrapper.contains(event.target)) {
        closePanel();
      }
    });
  });
});

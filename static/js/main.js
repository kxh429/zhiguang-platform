/* ====================================
   织光平台 - 全局交互脚本
   ==================================== */
(function () {
  "use strict";

  // ─── 移动端菜单切换 ───
  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener("click", function () {
      mobileMenu.classList.toggle("hidden");
    });
  }

  // ─── Flash 消息自动消失 ───
  const flashMessages = document.querySelectorAll(".flash-msg");
  if (flashMessages.length > 0) {
    setTimeout(function () {
      flashMessages.forEach(function (msg) {
        msg.style.transition = "opacity 0.3s, transform 0.3s";
        msg.style.opacity = "0";
        msg.style.transform = "translateX(120%)";
        setTimeout(function () {
          msg.remove();
        }, 300);
      });
    }, 3500);
  }

  // ─── Chart.js 全局默认样式 ───
  if (typeof Chart !== "undefined") {
    Chart.defaults.font.family = '"Noto Sans SC", sans-serif';
    Chart.defaults.color = "#9B9AA6";
    Chart.defaults.borderColor = "#2D2F45";
  }
})();

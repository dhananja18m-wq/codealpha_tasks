/**
 * ShopEase — main.js
 * Phase 1: UI Foundation + Animated Homepage
 *
 * Modules:
 *  1. Navbar (sticky scroll-compact, hamburger toggle)
 *  2. Hero Load Animations (staggered entrance)
 *  3. Parallax (subtle decorative element movement)
 *  4. Scroll Reveal (IntersectionObserver-based)
 *  5. Product Carousel (Vanilla JS, responsive)
 *  6. Wishlist Toggle (micro-interaction)
 *  7. Cart (counter animation)
 *  8. Back-to-Top Button
 *  9. Smooth Anchor Scrolling
 * 10. Newsletter Forms (frontend-only feedback)
 * 11. Active Nav Link on Scroll
 */

'use strict';

/* ============================================================
   UTILITY HELPERS
============================================================ */

/**
 * Check if the user prefers reduced motion.
 * All animation-heavy code should respect this.
 */
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/**
 * Throttle a function call to at most once per `limitMs`.
 * Used for scroll-heavy handlers.
 */
function throttle(fn, limitMs) {
  let lastRun = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastRun >= limitMs) {
      lastRun = now;
      fn.apply(this, args);
    }
  };
}

/**
 * Safely query a single element. Returns null without throwing.
 */
const $ = (selector, context = document) => context.querySelector(selector);
const $$ = (selector, context = document) => [...context.querySelectorAll(selector)];


/* ============================================================
   1. NAVBAR — Sticky compact state + Hamburger menu
============================================================ */
(function initNavbar() {
  const navbar    = $('#navbar');
  const hamburger = $('#hamburger');
  const mobileMenu = $('#mobile-menu');
  if (!navbar) return;

  // Compact state on scroll
  const handleNavbarScroll = throttle(() => {
    if (window.scrollY > 80) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }, 50);

  window.addEventListener('scroll', handleNavbarScroll, { passive: true });

  // Hamburger toggle
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('open', isOpen);
      hamburger.setAttribute('aria-expanded', String(isOpen));
      mobileMenu.setAttribute('aria-hidden', String(!isOpen));

      // Trap focus inside mobile menu when open
      if (isOpen) {
        const firstLink = mobileMenu.querySelector('a, input, button');
        if (firstLink) firstLink.focus();
      }
    });

    // Close mobile menu on any link click
    $$('.mobile-nav-link, .mobile-actions a', mobileMenu).forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
      });
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
        hamburger.focus();
      }
    });
  }
})();


/* ============================================================
   2. HERO LOAD ANIMATIONS — Staggered entrance on page load
============================================================ */
(function initHeroAnimations() {
  if (prefersReducedMotion) return;

  /**
   * Sequence of hero elements to animate in.
   * Each step: [element, delay-in-ms, optional-class-override]
   * Uses requestAnimationFrame for smooth, non-blocking animation start.
   */
  const steps = [
    { selector: '#hero-badge',    delay: 200 },
    { selector: '#hero-title',    delay: 380 },
    { selector: '#hero-subtitle', delay: 520 },
    { selector: '#hero-stats',    delay: 640 },
    { selector: '#hero-cta',      delay: 760 },
    { selector: '#hero-visual',   delay: 300 }, // starts early, longer duration
  ];

  steps.forEach(({ selector, delay }) => {
    const el = $(selector);
    if (!el) return;

    setTimeout(() => {
      requestAnimationFrame(() => {
        el.style.transition = `opacity 600ms cubic-bezier(0.4,0,0.2,1), transform 700ms cubic-bezier(0.4,0,0.2,1)`;
        el.classList.add('revealed');
      });
    }, delay);
  });

  // Float cards appear after hero visual
  setTimeout(() => {
    $$('.float-card').forEach((card, i) => {
      setTimeout(() => {
        requestAnimationFrame(() => {
          card.style.transition = 'opacity 500ms ease, transform 500ms ease';
          card.style.opacity = '1';
        });
      }, i * 200);
    });
  }, 800);
})();


/* ============================================================
   3. PARALLAX — Subtle hero background element movement
============================================================ */
(function initParallax() {
  if (prefersReducedMotion) return;

  const shapes = $$('.hero__bg-shapes .shape');
  if (!shapes.length) return;

  const handleParallax = throttle((e) => {
    const cx = window.innerWidth / 2;
    const cy = window.innerHeight / 2;
    const dx = (e.clientX - cx) / cx;   // -1 to +1
    const dy = (e.clientY - cy) / cy;   // -1 to +1

    shapes.forEach((shape, i) => {
      const factor = (i + 1) * 8;  // gentle layered depth
      const tx = dx * factor;
      const ty = dy * factor;
      shape.style.transform = `translate(${tx}px, ${ty}px)`;
    });
  }, 40);

  document.addEventListener('mousemove', handleParallax, { passive: true });
})();


/* ============================================================
   4. SCROLL REVEAL — IntersectionObserver for section reveals
============================================================ */
(function initScrollReveal() {
  const revealClasses = [
    '.reveal-fade-up',
    '.reveal-fade-in',
    '.reveal-slide-left',
    '.reveal-slide-right',
    '.reveal-scale',
  ];

  const targets = $$(revealClasses.join(', '));
  if (!targets.length) return;

  if (prefersReducedMotion) {
    // Immediately reveal all when reduced motion is preferred
    targets.forEach(el => el.classList.add('revealed'));
    return;
  }

  /**
   * IntersectionObserver: fires callback when element enters viewport.
   * threshold: element must be 12% visible before animating.
   * rootMargin: trigger slightly before the element enters viewport.
   */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        // Unobserve after revealing — saves memory and CPU
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px',
  });

  targets.forEach(el => observer.observe(el));
})();


/* ============================================================
   5. PRODUCT CAROUSEL — Responsive Vanilla JS carousel
============================================================ */
(function initCarousel() {
  const track      = $('#products-track');
  const btnPrev    = $('#carousel-prev');
  const btnNext    = $('#carousel-next');
  const dotsWrap   = $('#carousel-dots');
  const container  = $('#product-carousel-container');

  if (!track || !btnPrev || !btnNext) return;

  const cards = $$('.product-card', track);
  let currentIndex = 0;
  let visibleCount = getVisibleCount();
  let maxIndex = Math.max(0, cards.length - visibleCount);
  let touchStartX = 0;
  let isDragging = false;

  /**
   * Determine how many cards are visible based on viewport width.
   * This mirrors the CSS breakpoints:
   *   ≤640px  → 1 card
   *   ≤900px  → 2 cards
   *   ≤1100px → 3 cards
   *   >1100px → 4 cards
   */
  function getVisibleCount() {
    const w = window.innerWidth;
    if (w <= 640)  return 1;
    if (w <= 900)  return 2;
    if (w <= 1100) return 3;
    return 4;
  }

  /**
   * Calculate the pixel width of a single card including gap.
   */
  function getCardWidth() {
    if (!cards.length) return 0;
    const cardRect   = cards[0].getBoundingClientRect();
    const trackStyle = window.getComputedStyle(track);
    const gap        = parseFloat(trackStyle.gap) || 24;
    return cardRect.width + gap;
  }

  /**
   * Move the carousel track to the given index position.
   */
  function goTo(index) {
    visibleCount = getVisibleCount();
    maxIndex     = Math.max(0, cards.length - visibleCount);
    currentIndex = Math.max(0, Math.min(index, maxIndex));

    const offset = currentIndex * getCardWidth();
    track.style.transform = `translateX(-${offset}px)`;

    updateButtons();
    updateDots();
  }

  /**
   * Enable/disable prev & next buttons at edges.
   */
  function updateButtons() {
    btnPrev.disabled = currentIndex === 0;
    btnNext.disabled = currentIndex >= maxIndex;
    btnPrev.style.opacity = currentIndex === 0 ? '0.4' : '1';
    btnNext.style.opacity = currentIndex >= maxIndex ? '0.4' : '1';
  }

  /**
   * Create or update dot indicators.
   * Number of dots = number of reachable positions.
   */
  function buildDots() {
    dotsWrap.innerHTML = '';
    const totalDots = maxIndex + 1;
    for (let i = 0; i <= maxIndex; i++) {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot' + (i === currentIndex ? ' active' : '');
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', `Slide ${i + 1} of ${totalDots}`);
      dot.setAttribute('aria-selected', String(i === currentIndex));
      dot.addEventListener('click', () => goTo(i));
      dotsWrap.appendChild(dot);
    }
  }

  function updateDots() {
    const dots = $$('.carousel-dot', dotsWrap);
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === currentIndex);
      dot.setAttribute('aria-selected', String(i === currentIndex));
    });
  }

  // Button click handlers
  btnPrev.addEventListener('click', () => goTo(currentIndex - 1));
  btnNext.addEventListener('click', () => goTo(currentIndex + 1));

  // Touch swipe support (mobile)
  track.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    isDragging = true;
  }, { passive: true });

  track.addEventListener('touchend', (e) => {
    if (!isDragging) return;
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) {  // 40px threshold
      if (diff > 0) goTo(currentIndex + 1);
      else          goTo(currentIndex - 1);
    }
    isDragging = false;
  }, { passive: true });

  // Keyboard navigation on track
  track.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft')  { e.preventDefault(); goTo(currentIndex - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); goTo(currentIndex + 1); }
  });

  // Rebuild on resize to adapt to breakpoints
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      buildDots();
      goTo(Math.min(currentIndex, getVisibleCount() === getVisibleCount() ? currentIndex : 0));
    }, 200);
  }, { passive: true });

  // Initialize
  buildDots();
  goTo(0);
})();


/* ============================================================
   6. WISHLIST TOGGLE — Heart icon micro-interaction
============================================================ */
(function initWishlist() {
  const buttons = $$('.product-card__wishlist');
  // Track wishlist state in memory (no backend in Phase 1)
  const wishlistState = new Set();

  buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();  // don't bubble to card
      const icon = btn.querySelector('i');
      const productId = btn.id;

      if (wishlistState.has(productId)) {
        // Remove from wishlist
        wishlistState.delete(productId);
        btn.classList.remove('active');
        icon.className = 'ri-heart-line';
        btn.setAttribute('aria-label', 'Add to wishlist');

        // Small scale-down animation
        btn.style.transform = 'scale(0.85)';
        setTimeout(() => { btn.style.transform = ''; }, 200);
      } else {
        // Add to wishlist
        wishlistState.add(productId);
        btn.classList.add('active');
        icon.className = 'ri-heart-fill';
        btn.style.color = '#EF4444';
        btn.setAttribute('aria-label', 'Remove from wishlist');

        // Pulse animation
        btn.style.transform = 'scale(1.3)';
        setTimeout(() => { btn.style.transform = 'scale(0.95)'; }, 150);
        setTimeout(() => { btn.style.transform = ''; }, 300);
      }
    });
  });
})();


/* ============================================================
   7. CART — Counter update with bounce animation & AJAX backend sync
============================================================ */
(function initCart() {
  const badge   = $('#cart-badge');
  const cartBtn = $('#cart-btn');

  function updateCartBadge(newCount) {
    if (!badge) return;
    badge.textContent = newCount;

    // Bounce animation class trick
    badge.style.transform = 'scale(1.5)';
    badge.style.transition = 'transform 150ms ease';
    setTimeout(() => {
      badge.style.transform = '';
    }, 200);

    // Cart icon shake
    if (cartBtn) {
      cartBtn.style.transform = 'rotate(-15deg) scale(1.15)';
      setTimeout(() => { cartBtn.style.transform = ''; }, 300);
    }
  }

  // Delegated click handler for product card cart buttons
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.product-card__cart-btn');
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation();

    const productId = btn.getAttribute('data-product-id');
    if (!productId) return;

    const originalContent = btn.innerHTML;
    btn.innerHTML = '<i class="ri-loader-4-line ri-spin"></i> Adding...';
    btn.disabled = true;

    try {
      const response = await fetch(`/cart/add/${productId}/`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
          updateCartBadge(data.cart_count);
          btn.innerHTML = '<i class="ri-check-line"></i> Added!';
          btn.style.background = 'var(--color-success)';
          if (window.showToast) {
            window.showToast(data.message || 'Added to cart!', 'success');
          }
          setTimeout(() => {
            btn.innerHTML = originalContent;
            btn.style.background = '';
            btn.disabled = false;
          }, 1500);
          return;
        }
      }
      window.location.href = `/cart/add/${productId}/`;
    } catch (err) {
      console.error('Cart error:', err);
      window.location.href = `/cart/add/${productId}/`;
    }
  });
})();


/* ============================================================
   8. BACK TO TOP — Floating button with smooth scroll
============================================================ */
(function initBackToTop() {
  const btn = $('#back-to-top');
  if (!btn) return;

  const handleScroll = throttle(() => {
    if (window.scrollY > 300) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, 100);

  window.addEventListener('scroll', handleScroll, { passive: true });

  btn.addEventListener('click', () => {
    if (prefersReducedMotion) {
      window.scrollTo(0, 0);
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
})();


/* ============================================================
   9. SMOOTH ANCHOR SCROLLING
============================================================ */
(function initSmoothScroll() {
  // Handle all in-page hash links for smooth scroll
  document.addEventListener('click', (e) => {
    const anchor = e.target.closest('a[href^="#"]');
    if (!anchor) return;

    const targetId = anchor.getAttribute('href').slice(1);
    if (!targetId) return;

    const targetEl = document.getElementById(targetId);
    if (!targetEl) return;

    e.preventDefault();

    const navbar = $('#navbar');
    const navbarH = navbar ? navbar.offsetHeight : 0;
    const top = targetEl.getBoundingClientRect().top + window.scrollY - navbarH - 8;

    if (prefersReducedMotion) {
      window.scrollTo(0, top);
    } else {
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
})();


/* ============================================================
  10. NEWSLETTER FORMS — Frontend-only feedback
============================================================ */
(function initNewsletterForms() {
  const forms = $$('#newsletter-form, #newsletter-cta-form');

  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const input  = form.querySelector('input[type="email"]');
      const btn    = form.querySelector('button[type="submit"]');
      if (!input || !btn) return;

      const email = input.value.trim();
      if (!email || !/\S+@\S+\.\S+/.test(email)) {
        input.style.borderColor = '#EF4444';
        input.focus();
        setTimeout(() => { input.style.borderColor = ''; }, 2000);
        return;
      }

      // Success feedback
      const originalText = btn.innerHTML;
      btn.innerHTML = '<i class="ri-check-line"></i> Subscribed!';
      btn.style.background = 'var(--color-success)';
      btn.disabled = true;
      input.disabled = true;

      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.background = '';
        btn.disabled = false;
        input.disabled = false;
        input.value = '';
      }, 3000);
    });
  });
})();


/* ============================================================
  11. ACTIVE NAV LINK — Highlight active section on scroll
============================================================ */
(function initActiveNavLinks() {
  const sections = $$('section[id]');
  const navLinks = $$('.nav-link');
  if (!sections.length || !navLinks.length) return;

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach(link => {
          const href = link.getAttribute('href');
          link.classList.toggle('active', href === `#${id}`);
        });
      }
    });
  }, {
    threshold: 0.40,
    rootMargin: '-80px 0px -40% 0px',
  });

  sections.forEach(section => sectionObserver.observe(section));
})();


/* ============================================================
  12. PHASE 3 — TOAST NOTIFICATION SYSTEM
============================================================ */
window.showToast = function showToast(message, type = 'success') {
  const container = $('#toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;

  const iconClass = type === 'success' ? 'ri-checkbox-circle-fill' : (type === 'info' ? 'ri-information-fill' : 'ri-notification-badge-fill');

  toast.innerHTML = `
    <i class="${iconClass} toast-icon"></i>
    <span class="toast-message">${message}</span>
    <button class="toast-close" aria-label="Close notification"><i class="ri-close-line"></i></button>
  `;

  container.appendChild(toast);

  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.add('toast--show');
  });

  // Close handler
  const closeBtn = toast.querySelector('.toast-close');
  const removeToast = () => {
    toast.classList.remove('toast--show');
    setTimeout(() => { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 400);
  };

  closeBtn.addEventListener('click', removeToast);

  // Auto dismiss after 3.5s
  setTimeout(removeToast, 3500);
};


/* ============================================================
  13. PHASE 3 — QUANTITY SELECTOR
============================================================ */
(function initQuantitySelector() {
  const input = $('#qty-input');
  const btnMinus = $('#qty-minus');
  const btnPlus = $('#qty-plus');

  if (!input || !btnMinus || !btnPlus) return;

  const maxStock = parseInt(input.getAttribute('data-max') || '99', 10);

  function updateQty(newVal) {
    let val = parseInt(newVal, 10);
    if (isNaN(val) || val < 1) val = 1;
    if (val > maxStock) val = maxStock;

    input.value = val;
    btnMinus.disabled = val <= 1;
    btnPlus.disabled = val >= maxStock;
  }

  btnMinus.addEventListener('click', () => {
    updateQty(parseInt(input.value, 10) - 1);
  });

  btnPlus.addEventListener('click', () => {
    updateQty(parseInt(input.value, 10) + 1);
  });

  input.addEventListener('change', () => {
    updateQty(input.value);
  });

  // Initial check
  updateQty(input.value || 1);
})();


/* ============================================================
  14. PHASE 3 — PRODUCT GALLERY THUMBNAILS & HOVER ZOOM
============================================================ */
(function initProductGallery() {
  const mainImg = $('#detail-main-img');
  const mainWrap = $('#detail-main-img-wrap');
  const thumbs = $$('.gallery-thumb');

  if (!mainImg || !thumbs.length) return;

  // Thumbnail switching
  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      thumbs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });

      thumb.classList.add('active');
      thumb.setAttribute('aria-selected', 'true');

      const newSrc = thumb.getAttribute('data-src');
      if (newSrc) {
        mainImg.style.opacity = '0.5';
        setTimeout(() => {
          mainImg.src = newSrc;
          mainImg.style.opacity = '1';
        }, 150);
      }
    });
  });

  // Hover zoom lens positioning
  if (mainWrap && !prefersReducedMotion) {
    mainWrap.addEventListener('mousemove', (e) => {
      const rect = mainWrap.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      mainImg.style.transformOrigin = `${x}% ${y}%`;
    });

    mainWrap.addEventListener('mouseleave', () => {
      mainImg.style.transformOrigin = 'center center';
    });
  }
})();


/* ============================================================
  15. PHASE 3 — PRODUCT DETAILS TABS
============================================================ */
(function initProductTabs() {
  const tabBtns = $$('.product-tabs .tab-btn');
  const tabPanels = $$('.tab-panels .tab-panel');

  if (!tabBtns.length || !tabPanels.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('aria-controls');

      tabBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });

      tabPanels.forEach(p => {
        p.classList.remove('active');
      });

      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const targetPanel = $(`#${targetId}`);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });
})();


/* ============================================================
  16. PHASE 3 — DETAIL PAGE CTAS & WISHLIST
============================================================ */
(function initDetailActions() {
  const cartBtn = $('#detail-cart-btn');
  const buyNowBtn = $('#detail-buynow-btn');
  const wishlistBtn = $('#detail-wishlist-btn');
  const qtyInput = $('#qty-input');
  const badge = $('#cart-badge');

  if (cartBtn) {
    cartBtn.addEventListener('click', async () => {
      const productId = cartBtn.getAttribute('data-product-id');
      const qty = parseInt(qtyInput?.value || '1', 10);
      const productName = cartBtn.getAttribute('data-product-name') || 'Item';

      if (!productId) return;

      const originalHTML = cartBtn.innerHTML;
      cartBtn.innerHTML = '<i class="ri-loader-4-line ri-spin"></i> Adding...';
      cartBtn.disabled = true;

      try {
        const response = await fetch(`/cart/add/${productId}/?quantity=${qty}`, {
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (response.ok) {
          const data = await response.json();
          if (badge && data.cart_count !== undefined) {
            badge.textContent = data.cart_count;
            badge.style.transform = 'scale(1.5)';
            setTimeout(() => { badge.style.transform = ''; }, 200);
          }
          if (window.showToast) {
            window.showToast(`✓ Added ${qty}x <strong>${productName}</strong> to your cart!`, 'success');
          }
          cartBtn.innerHTML = '<i class="ri-check-line"></i> Added!';
          cartBtn.style.background = 'var(--color-success)';
          setTimeout(() => {
            cartBtn.innerHTML = originalHTML;
            cartBtn.style.background = '';
            cartBtn.disabled = false;
          }, 1500);
        } else {
          window.location.href = `/cart/add/${productId}/?quantity=${qty}`;
        }
      } catch (err) {
        console.error('Detail cart add error:', err);
        window.location.href = `/cart/add/${productId}/?quantity=${qty}`;
      }
    });
  }

  if (buyNowBtn) {
    buyNowBtn.addEventListener('click', async () => {
      const productId = buyNowBtn.getAttribute('data-product-id');
      const qty = parseInt(qtyInput?.value || '1', 10);
      if (productId) {
        try {
          await fetch(`/cart/add/${productId}/?quantity=${qty}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
          });
        } catch (e) {
          console.error('BuyNow error:', e);
        }
      }
      window.location.href = '/checkout/';
    });
  }

  if (wishlistBtn) {
    wishlistBtn.addEventListener('click', () => {
      const isWish = wishlistBtn.classList.toggle('active');
      const icon = wishlistBtn.querySelector('i');
      if (icon) {
        icon.className = isWish ? 'ri-heart-fill' : 'ri-heart-line';
      }

      wishlistBtn.style.transform = 'scale(1.25)';
      setTimeout(() => { wishlistBtn.style.transform = ''; }, 250);

      if (window.showToast) {
        if (isWish) {
          window.showToast(`❤️ Added item to your wishlist!`, 'success');
        } else {
          window.showToast(`Removed item from your wishlist.`, 'info');
        }
      }
    });
  }
})();


/* ============================================================
   INITIALIZATION LOG
============================================================ */
console.log('%cShopEase Phase 3 — Product Details JS Initialized', 'color:#FF6B00; font-weight:700; font-size:14px;');


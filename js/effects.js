/* ==========================================
   ПУТЬ В АД — JavaScript эффекты
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {
    initDepthIndicator();
    initFadeIn();
    initGlitchText();
    initSmoothScroll();
    initParallax();
});

/* ==========================================
   DEPTH INDICATOR — Индикатор глубины/скролла
   ========================================== */

function initDepthIndicator() {
    const indicator = document.querySelector('.depth-indicator');
    const label = document.querySelector('.depth-label');

    if (!indicator) return;

    function updateDepth() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;

        document.documentElement.style.setProperty('--scroll-progress', `${scrollPercent}%`);

        if (label) {
            // Update depth label based on scroll
            const depth = Math.round(scrollPercent);
            label.textContent = `ГЛУБИНА: ${depth}%`;
        }
    }

    window.addEventListener('scroll', updateDepth, { passive: true });
    updateDepth();
}

/* ==========================================
   FADE IN ON SCROLL — Появление при скролле
   ========================================== */

function initFadeIn() {
    const fadeElements = document.querySelectorAll('.fade-in, .fade-in-stagger');

    if (fadeElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optionally unobserve after animation
                // observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    fadeElements.forEach(el => observer.observe(el));
}

/* ==========================================
   GLITCH TEXT — Инициализация глитч-текста
   ========================================== */

function initGlitchText() {
    const glitchElements = document.querySelectorAll('.glitch');

    glitchElements.forEach(el => {
        // Set data-text attribute for CSS pseudo-elements
        el.setAttribute('data-text', el.textContent);
    });
}

/* ==========================================
   SMOOTH SCROLL — Плавный скролл
   ========================================== */

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/* ==========================================
   PARALLAX — Параллакс-эффект
   ========================================== */

function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');

    if (parallaxElements.length === 0) return;

    function updateParallax() {
        const scrollTop = window.scrollY;

        parallaxElements.forEach(el => {
            const speed = el.dataset.speed || 0.5;
            const yPos = -(scrollTop * speed);
            el.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });
    }

    window.addEventListener('scroll', updateParallax, { passive: true });
}

/* ==========================================
   RANDOM GLITCH — Случайный глитч
   ========================================== */

function triggerRandomGlitch() {
    const elements = document.querySelectorAll('h1, h2, .ember-text');
    if (elements.length === 0) return;

    const randomEl = elements[Math.floor(Math.random() * elements.length)];

    randomEl.style.textShadow = '2px 0 var(--ember), -2px 0 var(--rust)';
    randomEl.style.transform = 'translate(-2px, 1px)';

    setTimeout(() => {
        randomEl.style.textShadow = '';
        randomEl.style.transform = '';
    }, 100);
}

// Trigger random glitch occasionally
setInterval(() => {
    if (Math.random() > 0.7) {
        triggerRandomGlitch();
    }
}, 5000);

/* ==========================================
   EMBER CURSOR — Угольки за курсором (опционально)
   ========================================== */

function initEmberCursor() {
    const container = document.createElement('div');
    container.className = 'cursor-embers';
    container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;';
    document.body.appendChild(container);

    let lastX = 0, lastY = 0;

    document.addEventListener('mousemove', (e) => {
        const dx = e.clientX - lastX;
        const dy = e.clientY - lastY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > 30) {
            createEmber(e.clientX, e.clientY, container);
            lastX = e.clientX;
            lastY = e.clientY;
        }
    });
}

function createEmber(x, y, container) {
    const ember = document.createElement('div');
    ember.style.cssText = `
        position: absolute;
        left: ${x}px;
        top: ${y}px;
        width: 4px;
        height: 4px;
        background: var(--ember);
        border-radius: 50%;
        pointer-events: none;
        box-shadow: 0 0 6px var(--ember), 0 0 12px var(--ember-dark);
        animation: ember-fade 1s ease-out forwards;
    `;
    container.appendChild(ember);

    setTimeout(() => ember.remove(), 1000);
}

// Add CSS for ember fade
const style = document.createElement('style');
style.textContent = `
    @keyframes ember-fade {
        0% { opacity: 1; transform: scale(1) translateY(0); }
        100% { opacity: 0; transform: scale(0.5) translateY(-30px); }
    }
`;
document.head.appendChild(style);

/* ==========================================
   TYPING EFFECT — Эффект печати (для эпиграфов)
   ========================================== */

function typeText(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    element.style.visibility = 'visible';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

/* ==========================================
   PAGE TRANSITION — Переход между страницами
   ========================================== */

function initPageTransitions() {
    // Add burn-out effect on link click
    document.querySelectorAll('a:not([href^="#"])').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (!href || href.startsWith('http') || href.startsWith('mailto')) return;

            e.preventDefault();
            document.body.classList.add('burn-out');

            setTimeout(() => {
                window.location.href = href;
            }, 500);
        });
    });

    // Add burn-in effect on page load
    document.body.classList.add('burn-in');
}

// Initialize page transitions
initPageTransitions();

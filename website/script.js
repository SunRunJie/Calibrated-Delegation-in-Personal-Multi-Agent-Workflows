const root = document.documentElement;
const header = document.querySelector('[data-header]');
const progress = document.querySelector('.reading-progress span');
const themeButton = document.querySelector('[data-theme-toggle]');
const menuButton = document.querySelector('[data-menu-button]');
const mobileMenu = document.querySelector('[data-mobile-menu]');
const figureDialog = document.querySelector('[data-figure-dialog]');
const dialogImage = document.querySelector('[data-dialog-image]');
const dialogCaption = document.querySelector('[data-dialog-caption]');

const savedTheme = localStorage.getItem('calibrated-theme');
if (savedTheme === 'dark' || savedTheme === 'light') root.dataset.theme = savedTheme;

function updateScroll() {
  const scrollable = document.documentElement.scrollHeight - innerHeight;
  const ratio = scrollable > 0 ? scrollY / scrollable : 0;
  progress.style.width = `${Math.min(100, ratio * 100)}%`;
  header.classList.toggle('scrolled', scrollY > 24);
}

themeButton?.addEventListener('click', () => {
  const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
  root.dataset.theme = next;
  localStorage.setItem('calibrated-theme', next);
});

menuButton?.addEventListener('click', () => {
  const open = mobileMenu.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});

mobileMenu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
  mobileMenu.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
}));

document.querySelectorAll('[data-figure]').forEach((button) => button.addEventListener('click', () => {
  dialogImage.src = button.dataset.figure;
  dialogImage.alt = button.dataset.caption || 'Expanded research figure';
  dialogCaption.textContent = button.dataset.caption || '';
  figureDialog.showModal();
}));

document.querySelector('[data-dialog-close]')?.addEventListener('click', () => figureDialog.close());
figureDialog?.addEventListener('click', (event) => {
  if (event.target === figureDialog) figureDialog.close();
});

document.querySelector('[data-copy-citation]')?.addEventListener('click', async (event) => {
  const button = event.currentTarget;
  try {
    await navigator.clipboard.writeText(button.dataset.copyText);
    const previous = button.innerHTML;
    button.textContent = 'Citation copied ✓';
    setTimeout(() => { button.innerHTML = previous; }, 1800);
  } catch {
    button.textContent = 'Select citation above';
  }
});

const observer = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 }) : null;

document.querySelectorAll('[data-reveal]').forEach((element) => {
  if (observer) observer.observe(element);
  else element.classList.add('revealed');
});

addEventListener('scroll', updateScroll, { passive: true });
updateScroll();

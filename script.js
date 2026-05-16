const startButton = document.getElementById('startButton');
const contactForm = document.getElementById('contactForm');
const navToggle = document.getElementById('navToggle');
const mobileMenu = document.getElementById('mobileMenu');
const scrollLinks = document.querySelectorAll('a[href^="#"]');
const contactMessage = document.getElementById('contactMessage');

const setMessage = (message, type = 'success') => {
  if (!contactMessage) return;
  contactMessage.textContent = message;
  contactMessage.className = `form-message ${type}`;
};

if (navToggle && mobileMenu) {
  navToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
}

scrollLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector(link.hash);
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth' });
    mobileMenu?.classList.remove('open');
  });
});

if (startButton) {
  startButton.addEventListener('click', () => {
    document.querySelector('#contact')?.scrollIntoView({ behavior: 'smooth' });
    mobileMenu?.classList.remove('open');
  });
}

if (contactForm) {
  contactForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const name = document.getElementById('nameInput')?.value.trim();
    const email = document.getElementById('emailInput')?.value.trim();

    if (!name || !email) {
      setMessage('Please provide your name and email.', 'error');
      return;
    }

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email })
      });

      if (!response.ok) {
        const errorBody = await response.json();
        throw new Error(errorBody.error || 'Submission failed');
      }

      setMessage('Thanks! Your request has been saved, and we will contact you soon.', 'success');
      contactForm.reset();
    } catch (error) {
      setMessage(error.message || 'Unable to submit form right now.', 'error');
    }
  });
}

const navLinks = document.querySelectorAll('.site-nav a');
const sections = document.querySelectorAll('section[id]');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      const id = entry.target.id;
      const navLink = document.querySelector(`.site-nav a[href="#${id}"]`);
      if (!navLink) return;
      if (entry.isIntersecting) {
        navLinks.forEach((link) => link.classList.remove('active'));
        navLink.classList.add('active');
      }
    });
  },
  {
    threshold: 0.45,
  }
);

sections.forEach((section) => observer.observe(section));

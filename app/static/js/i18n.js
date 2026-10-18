/**
 * AstroLogic AI — Client-Side Dynamic i18n Translation Engine
 */

window.AstroI18n = {
  currentLang: 'en',
  translations: {},

  init: function () {
    const cookieMatch = document.cookie.match(/(?:^|; )lang=([^;]*)/);
    const savedLang = cookieMatch ? cookieMatch[1] : (localStorage.getItem('lang') || 'en');
    this.currentLang = savedLang;

    // Attach listener to any language selector dropdown
    const selectors = document.querySelectorAll('.lang-select');
    selectors.forEach(select => {
      select.value = this.currentLang;
      select.addEventListener('change', (e) => {
        this.switchLanguage(e.target.value);
      });
    });
  },

  switchLanguage: function (newLang) {
    if (!newLang) return;
    this.currentLang = newLang;
    localStorage.setItem('lang', newLang);
    document.cookie = `lang=${newLang}; path=/; max-age=31536000`;

    // Fetch locale translation dictionary and update UI instantly
    fetch(`/api/locales/${newLang}`)
      .then(res => res.json())
      .then(data => {
        if (data && data.translations) {
          this.translations = data.translations;
          this.applyTranslations();
        }
        // Update URL path if prefix is used
        const pathParts = window.location.pathname.split('/').filter(Boolean);
        const supported = ['en', 'hi', 'mr', 'gu', 'ta', 'te', 'kn', 'bn'];
        if (pathParts.length > 0 && supported.includes(pathParts[0])) {
          pathParts[0] = newLang;
          window.location.pathname = '/' + pathParts.join('/');
        }
      })
      .catch(err => console.warn('Locale fetch error:', err));
  },

  applyTranslations: function () {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (this.translations[key]) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.placeholder = this.translations[key];
        } else {
          el.textContent = this.translations[key];
        }
      }
    });
    document.documentElement.lang = this.currentLang;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  window.AstroI18n.init();
});

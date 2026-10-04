(function () {
  const SLIDE_COUNT = 12;
  const AUTO_ADVANCE_MS = 5000;
  const ASSET_VERSION = 3; // bump when a testimonial image is swapped/reordered, to bust browser cache

  const track = document.getElementById('carouselTrack');
  const dotsWrap = document.getElementById('carouselDots');
  const prevBtn = document.getElementById('carouselPrev');
  const nextBtn = document.getElementById('carouselNext');
  const carousel = document.getElementById('carousel');

  let current = 0;
  let timer = null;

  for (let i = 1; i <= SLIDE_COUNT; i++) {
    const num = String(i).padStart(2, '0');

    const slide = document.createElement('div');
    slide.className = 'carousel__slide';
    const img = document.createElement('img');
    img.src = `assets/provas-sociais/prova-social-${num}.png?v=${ASSET_VERSION}`;
    img.alt = `Depoimento de cliente ${i}`;
    slide.appendChild(img);
    track.appendChild(slide);

    const dot = document.createElement('button');
    dot.className = 'carousel__dot';
    dot.setAttribute('aria-label', `Ir para o depoimento ${i}`);
    dot.addEventListener('click', () => goTo(i - 1));
    dotsWrap.appendChild(dot);
  }

  const dots = Array.from(dotsWrap.children);

  function render() {
    track.style.transform = `translateX(-${current * 100}%)`;
    dots.forEach((d, idx) => d.classList.toggle('carousel__dot--active', idx === current));
  }

  function goTo(index) {
    current = (index + SLIDE_COUNT) % SLIDE_COUNT;
    render();
    restartTimer();
  }

  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  function restartTimer() {
    if (timer) clearInterval(timer);
    timer = setInterval(next, AUTO_ADVANCE_MS);
  }

  nextBtn.addEventListener('click', next);
  prevBtn.addEventListener('click', prev);
  carousel.addEventListener('mouseenter', () => clearInterval(timer));
  carousel.addEventListener('mouseleave', restartTimer);

  render();
  restartTimer();

  // ---------- Image placeholders: auto-upgrade when the real file shows up ----------
  function upgradePlaceholder(el) {
    el.querySelectorAll('img').forEach((img) => img.remove());
    el.classList.remove('img-placeholder--filled');
    const testImg = new Image();
    testImg.onload = () => {
      const img = document.createElement('img');
      img.src = el.dataset.src;
      img.alt = el.dataset.label || '';
      el.appendChild(img);
      el.classList.add('img-placeholder--filled');
    };
    testImg.onerror = () => {}; // stays a placeholder
    testImg.src = el.dataset.src;
  }

  document.querySelectorAll('.img-placeholder[data-src]').forEach(upgradePlaceholder);

  // ---------- Combination simulator ----------
  const SIM_CATEGORIES = [
    { slug: 'terapeuticos', label: 'Terapêuticos' },
    { slug: 'decorados', label: 'Decorados' },
    { slug: 'espirituais', label: 'Espirituais' },
    { slug: 'fitoenergeticos', label: 'Fitoenergéticos' },
    { slug: 'frutas', label: 'Formato de Frutas' },
    { slug: 'veganos', label: 'Veganos' },
  ];

  const SIM_CAPTIONS = {
    'decorados|espirituais': 'Ritual bonito de se ver.',
    'decorados|fitoenergeticos': 'Intenção com camada marmorizada.',
    'decorados|frutas': 'Vitrine que ninguém resiste.',
    'decorados|terapeuticos': 'Relaxa e ainda decora.',
    'decorados|veganos': 'Visual forte, consciência limpa.',
    'espirituais|fitoenergeticos': 'Dobro de intenção, dobro de energia.',
    'espirituais|frutas': 'Ritual com cara de doce.',
    'espirituais|terapeuticos': 'Calma com propósito.',
    'espirituais|veganos': 'Intenção 100% natural.',
    'fitoenergeticos|frutas': 'Prosperidade que chama atenção.',
    'fitoenergeticos|terapeuticos': 'Energia e relaxamento juntos.',
    'fitoenergeticos|veganos': 'Intenção sem origem animal.',
    'frutas|terapeuticos': 'Doce por fora, calmo por dentro.',
    'frutas|veganos': 'Parece doce, é vegano.',
    'terapeuticos|veganos': 'Relaxa com consciência.',
  };

  const simA = document.getElementById('simCatA');
  const simB = document.getElementById('simCatB');

  if (simA && simB) {
    SIM_CATEGORIES.forEach((c) => {
      const optA = document.createElement('option');
      optA.value = c.slug;
      optA.textContent = c.label;
      simA.appendChild(optA);

      const optB = document.createElement('option');
      optB.value = c.slug;
      optB.textContent = c.label;
      simB.appendChild(optB);
    });
    simA.selectedIndex = 0;
    simB.selectedIndex = 1;

    const simResultImg = document.getElementById('simResultImg');
    const simCaption = document.getElementById('simCaption');
    const simResult = document.getElementById('simResult');

    document.getElementById('simGo').addEventListener('click', () => {
      const a = simA.value;
      const b = simB.value;

      if (a === b) {
        simCaption.textContent = 'Escolha duas categorias diferentes.';
        return;
      }

      const slugs = [a, b].sort();
      const key = slugs.join('|');
      const labelA = SIM_CATEGORIES.find((c) => c.slug === a).label;
      const labelB = SIM_CATEGORIES.find((c) => c.slug === b).label;

      simResultImg.dataset.src = `assets/simulador/combo-${slugs.join('-')}.png`;
      simResultImg.dataset.label = `combo-${slugs.join('-')}.png`;
      upgradePlaceholder(simResultImg);

      simCaption.textContent = `${labelA} + ${labelB} — ${SIM_CAPTIONS[key] || 'combinação exclusiva sua.'}`;

      // retrigger the reveal animation even on repeated clicks
      simResult.classList.remove('simulator__result--reveal');
      void simResult.offsetWidth;
      simResult.classList.add('simulator__result--reveal');
    });
  }

  // ---------- FAQ accordion (single-open) ----------
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach((btn) => {
    btn.addEventListener('click', () => {
      const isOpen = btn.classList.contains('faq-item--open');
      faqItems.forEach((other) => {
        other.classList.remove('faq-item--open');
        const ans = other.querySelector('.faq-item__answer');
        if (ans) ans.remove();
      });
      if (!isOpen) {
        btn.classList.add('faq-item--open');
        const ans = document.createElement('span');
        ans.className = 'faq-item__answer';
        ans.textContent = btn.dataset.a;
        btn.appendChild(ans);
      }
    });
  });
})();

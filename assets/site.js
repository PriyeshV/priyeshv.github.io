(() => {
 const path = location.pathname.replace(/index\.html$/, '').replace(/\/$/, '');
 document.querySelectorAll('nav a').forEach(a => {
  if (new URL(a.href).pathname.replace(/\/$/, '') === path) a.setAttribute('aria-current', 'page');
 });
 const search = document.querySelector('#search');
 if (!search) return;
 const topic = document.querySelector('#topic');
 const year = document.querySelector('#year');
 const pubs = [...document.querySelectorAll('.pub')];
 const filter = () => {
  let count = 0;
  for (const pub of pubs) {
   const match = pub.textContent.toLowerCase().includes(search.value.trim().toLowerCase()) && (!topic.value || pub.dataset.topic === topic.value) && (!year.value || pub.dataset.year === year.value);
   pub.hidden = !match;
   if (match) count++;
  }
  document.querySelector('#result-count').textContent = `${count} of ${pubs.length} records`;
  document.querySelector('#empty').hidden = count !== 0;
 };
 [search, topic, year].forEach(el => el.addEventListener('input', filter));
 filter();
})();

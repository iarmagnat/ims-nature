const popup = document.getElementById('image-popup');
const container = document.getElementById('image-popup-container');

const clickableImages = document.querySelectorAll('[data-clickable-image]');

const hidePopup = () => {
  popup.classList.remove('image-popup--active');
};

const showPopup = e => {
  const image = e.target;
  const src = image.src;
  const alt = image.alt;
  const title = image.title || alt;
  container.innerHTML = `<img src="${src}" alt="${alt}" title="${title}" class="image-popup__image"/>`;
  popup.classList.add('image-popup--active');
};

popup.addEventListener('click', hidePopup);

clickableImages.forEach(image => {
  image.addEventListener('click', showPopup);
});
document.addEventListener('click', function(e){
  const card = e.target.closest('.incident-card');
  if(!card) return;
  // Toggle collapsed state when header clicked
  if(e.target.closest('.card-header')){
    card.classList.toggle('collapsed');
    const body = card.querySelector('.card-body');
    if(card.classList.contains('collapsed')) body.style.display = 'none';
    else body.style.display = '';
  }
});

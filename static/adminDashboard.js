const cancelSub = document.getElementById('cancel-sub')
const addSubBtn = document.getElementById('add-sub-btn')
const addSub = document.getElementById('add-sub')

addSubBtn.addEventListener('click', () => {
  addSub.style.display = 'flex'
})

cancelSub.addEventListener('click', () => {
  addSub.style.display = 'none'
})

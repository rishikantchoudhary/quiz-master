const cancelSub = document.getElementById('cancel-sub')
const addSubBtn = document.getElementById('add-sub-btn')
const addSub = document.getElementById('add-sub')

addSubBtn.addEventListener('click', () => {
  addSub.style.display = 'flex'
})

cancelSub.addEventListener('click', () => {
  addSub.style.display = 'none'
})

// delete sub
function deleteSub(id) {
  fetch(`/delete-sub`, {
    method: 'POST',
    body: JSON.stringify({ sub_id: id }),
  }).then((res) => {
    if (res.ok) {
      window.location.href = '/dashboard'
    }
  })
}

// delete chapter
function deleteChap(id) {
  fetch(`/delete-chap`, {
    method: 'POST',
    body: JSON.stringify({ chap_id: id }),
  }).then((res) => {
    if (res.ok) {
      window.location.href = '/dashboard'
    }
  })
}

// add chapter
function addChap(sub_id) {
  window.location.href = `/add-chapter/${sub_id}`
}

const cancelQuiz = document.getElementById('cancel-quiz')
const addQuizBtn = document.getElementById('add-quiz-btn')
const addQuiz = document.getElementById('add-quiz')

addQuizBtn.addEventListener('click', () => {
  addQuiz.style.display = 'flex'
})

cancelQuiz.addEventListener('click', () => {
  addQuiz.style.display = 'none'
})

// delete quiz
function deleteQuiz(id) {
  fetch(`/delete-quiz`, {
    method: 'POST',
    body: JSON.stringify({ quiz_id: id }),
  }).then((res) => {
    if (res.ok) {
      window.location.href = '/admin-quiz'
    }
  })
}

// edit quiz
function editQuiz(id) {
  window.location.href = `/edit-quiz/${id}`
}

// view quiz
function viewQuiz(id) {
  window.location.href = `/view-quiz/${id}`
}

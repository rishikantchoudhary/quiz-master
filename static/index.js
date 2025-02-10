try {
  const alert = document.getElementById('alert')
  const close = document.getElementById('close-alert')

  close.addEventListener('click', () => {
    alert.style.display = 'none'
  })

  setTimeout(() => {
    alert.style.display = 'none'
  }, 3000)
} catch (error) {}

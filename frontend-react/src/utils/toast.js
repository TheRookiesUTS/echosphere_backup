// Simple toast notification utility
export const toast = {
  success: (title, message = '') => {
    showToast(title, message, 'success')
  },
  error: (title, message = '') => {
    showToast(title, message, 'error')
  },
  info: (title, message = '') => {
    showToast(title, message, 'info')
  },
}

function showToast(title, message, type) {
  const colors = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
  }

  const toast = document.createElement('div')
  toast.className = `fixed top-20 right-5 ${colors[type]} text-white px-6 py-4 rounded-lg shadow-lg z-[10000] animate-fadeInUp max-w-sm`
  toast.innerHTML = `
    <div class="font-semibold mb-1">${title}</div>
    ${message ? `<div class="text-sm opacity-90">${message}</div>` : ''}
  `

  document.body.appendChild(toast)

  setTimeout(() => {
    toast.style.opacity = '0'
    toast.style.transform = 'translateY(-20px)'
    toast.style.transition = 'all 0.3s ease-out'
    setTimeout(() => {
      document.body.removeChild(toast)
    }, 300)
  }, 3000)
}


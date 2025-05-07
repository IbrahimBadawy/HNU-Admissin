export function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.innerText = message;
  
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = 9999;
    toast.style.padding = '10px 20px';
    toast.style.borderRadius = '8px';
    toast.style.color = 'white';
    toast.style.fontWeight = 'bold';
    toast.style.boxShadow = '0 4px 10px rgba(0,0,0,0.2)';
    toast.style.backgroundColor = type === 'success' ? '#16a34a' : '#dc2626';
    toast.style.transition = 'opacity 0.5s ease';
  
    document.body.appendChild(toast);
  
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 500);
    }, 3000);
  }
  
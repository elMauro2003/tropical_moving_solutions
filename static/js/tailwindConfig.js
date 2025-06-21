tailwind.config = {
    theme: {
      extend: {
        keyframes: {
          fadeIn: {
            '0%': { opacity: '0' },
            '100%': { opacity: '1' }
          },
          bounce: {
            '0%, 100%': { transform: 'translateY(0)' },
            '50%': { transform: 'translateY(-15px)' }
          },
          float: {
            '0%, 100%': { transform: 'translateY(0)' },
            '50%': { transform: 'translateY(-15px)' }
          }
        },
        animation: {
          fadeIn: 'fadeIn 1.5s ease-in-out',
          bounce: 'bounce 1.5s infinite',
          float: 'float 3s ease-in-out infinite'
        }
      }
    }
  }
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los enlaces de navegación
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Función para manejar el clic
    function handleNavClick(event) {
        
        // Remover clase 'active' de todos los enlaces
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // Añadir clase 'active' al enlace clickeado
        this.classList.add('active');
    }
    
    // Añadir event listener a cada enlace
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavClick);
    });
});
    // Imágenes
const images = [
'static/1.jpg',
'static/2.jpg',
'static/3.jpg',
'static/4.jpg',
'static/5.jpg'
];

// Obtener elementos del DOM
const carousel = document.getElementById('carousel');
let currentIndex = 0;

// Crear elementos de imagen para el carrusel
images.forEach((src, index) => {
const imgDiv = document.createElement('div');
imgDiv.className = `carousel-item ${index === 0 ? 'active' : ''}`;
imgDiv.style.backgroundImage = `url(${src})`;
imgDiv.dataset.index = index;
carousel.appendChild(imgDiv);
});

// Función para cambiar las imágenes
function changeBackground() {
// Ocultar imagen actual
const currentImg = document.querySelector('.carousel-item.active');
if (currentImg) {
    currentImg.classList.remove('active');
}

// Calcular siguiente índice
currentIndex = (currentIndex + 1) % images.length;

// Mostrar siguiente imagen
const nextImg = document.querySelector(`.carousel-item[data-index="${currentIndex}"]`);
if (nextImg) {
    nextImg.classList.add('active');
}
}

// Iniciar el carrusel
setTimeout(() => {
// Cambiar imagen cada 5 segundos
setInterval(changeBackground, 3000);
}, 1000);

// Animación de entrada para la tarjeta
document.addEventListener('DOMContentLoaded', () => {
const card = document.getElementById('card');
card.classList.add('animate-fadeIn');
});

// Función para el scroll hacia abajo
document.getElementById('scroll-down').addEventListener('click', () => {
const nextSection = document.getElementById('sobre-nosotros');
if (nextSection) {
    nextSection.scrollIntoView({ behavior: 'smooth' });
}
});

// Agregar efecto de teclado para scroll
document.addEventListener('keydown', (e) => {
if (e.key === 'ArrowDown') {
    const nextSection = document.getElementById('sobre-nosotros');
    if (nextSection) {
    nextSection.scrollIntoView({ behavior: 'smooth' });
    }
}
});
// Toggle Mobile Menu
const menuBtn = document.getElementById('menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
}

// Elementos de la lista
const elementos = document.querySelectorAll(".elemento");
const infoContainers = document.querySelectorAll(".info-container");

// Mostrar sección activa
function showSection(targetId) {
    // Actualizar elementos de la lista
    elementos.forEach(el => {
        el.classList.remove("w-[230px]", "border-b-orange-700", "font-bold");
        el.classList.add("border-b-orange-600");
    });
    
    // Actualizar contenedores
    infoContainers.forEach(container => {
        if (container.id === targetId) {
            container.classList.remove("translate-x-full", "opacity-0");
            container.classList.add("translate-x-0", "opacity-100");
        } else {
            container.classList.remove("translate-x-0", "opacity-100");
            container.classList.add("translate-x-full", "opacity-0");
        }
    });
    
    // Resaltar elemento activo
    const activeElement = Array.from(elementos).find(el => el.dataset.target === targetId);
    if (activeElement) {
        activeElement.classList.add("w-[230px]", "border-b-orange-700", "font-bold");
        activeElement.classList.remove("border-b-orange-600");
    }
}

// Eventos para elementos de la lista
elementos.forEach(elemento => {
    elemento.addEventListener("click", () => {
        const targetId = elemento.dataset.target;
        showSection(targetId);
    });
});

// Inicializar con la primera sección activa
showSection('tropical');
        document.addEventListener('DOMContentLoaded', function() {
    const testimonials = document.querySelectorAll('.testimonial-card');
    const dots = document.querySelectorAll('.dot');
    let currentIndex = 0;
    let interval;
    
    // Function to show testimonial
    function showTestimonial(index) {
        // Hide all testimonials
        testimonials.forEach(testimonial => {
            testimonial.classList.remove('active');
        });
        
        // Remove active class from all dots
        dots.forEach(dot => {
            dot.classList.remove('active');
        });
        
        // Show selected testimonial
        testimonials[index].classList.add('active');
        
        // Activate corresponding dot
        dots[index].classList.add('active');
        
        // Update current index
        currentIndex = index;
    }
    
    // Function to show next testimonial
    function nextTestimonial() {
        const nextIndex = (currentIndex + 1) % testimonials.length;
        showTestimonial(nextIndex);
    }
    
    // Start automatic slider
    function startSlider() {
        interval = setInterval(nextTestimonial, 5000);
    }
    
    // Initialize slider
    function initSlider() {
        // Show first testimonial
        showTestimonial(0);
        
        // Start automatic slider
        startSlider();
        
        // Add click event to dots
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                clearInterval(interval);
                showTestimonial(index);
                startSlider();
            });
        });
    }
    
    // Initialize the slider
    initSlider();
});
  
const greetings = [
  "• Hola", "• Bonjour", "• Kon'nichiwa", "• Hallo", "• Olá",
  "• Hej", "• Nǐ hǎo", "• Merhaba","• Sawubona", 
  "• Dia Duit", "• 你好", "• привет", "• Halo",
];

const finalGreeting = "• नमस्ते";
const greetingElement = document.getElementById("greeting");
const greetingContainer = document.querySelector(".greeting-container");
const mainContent = document.getElementById("main-content");
const navbar = document.querySelector(".navbar");

let index = 0;
let delay = 200; // Faster initial delay

function showNextGreeting() {
  if (index < greetings.length) {
    greetingElement.textContent = greetings[index];
    index++;
    delay *= 0.9; // Speed up slightly
    setTimeout(showNextGreeting, delay);
  } else {
    greetingElement.textContent = finalGreeting;
    setTimeout(() => {
      greetingContainer.style.transform = "translateY(-100%)"; // Slide up
      greetingContainer.style.opacity = 0; // Fade out
      setTimeout(() => {
        greetingContainer.style.display = "none"; // Hide the greeting container to allow scrolling
        navbar.style.display = "flex"; // Show the navbar
        mainContent.style.display = "block"; // Show main content
        setTimeout(() => {
          mainContent.style.opacity = 1; // Fade in main content
        }, 100); // Small delay for smooth transition
      }, 500); // Wait for slide-up animation to complete
    }, 1000); // Wait before sliding up
  }
}

window.onload = () => {
  mainContent.style.display = "none"; // Hide main content initially
  navbar.style.display = "none"; // Ensure navbar is fully hidden
  greetingContainer.style.transition = "transform 0.5s ease-in-out, opacity 0.5s ease-in-out"; // Smooth slide and fade
  mainContent.style.transition = "opacity 0.5s ease-in-out"; // Smooth fade
  mainContent.style.opacity = 0;
  setTimeout(showNextGreeting, delay);
};

const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("light-mode"); // Toggle light mode class
  if (document.body.classList.contains("light-mode")) {
    themeIcon.src = "/sun-outline.svg"; // Switch to sun icon
    navbar.style.backgroundColor = "#dddddd"; // Light mode navbar background
    greetingContainer.style.backgroundColor = "#dddddd"; // Light mode greeting container background
  } else {
    themeIcon.src = "/moon-outline.svg"; // Switch to moon icon
    navbar.style.backgroundColor = "#3a3a3a"; // Dark mode navbar background
    greetingContainer.style.backgroundColor = "#3a3a3a"; // Dark mode greeting container background
  }
});

// Ensure the site starts in dark mode
document.body.classList.remove("light-mode");
themeIcon.src = "/moon-outline.svg"; // Default icon for dark mode
navbar.style.backgroundColor = "#3a3a3a"; // Ensure navbar starts with dark mode background
greetingContainer.style.backgroundColor = "#3a3a3a"; // Ensure greeting container starts with dark mode background

function showTimeline(type) {
  const workTab = document.getElementById('work-tab');
  const eduTab = document.getElementById('education-tab');
  const workTimeline = document.getElementById('work-timeline');
  const eduTimeline = document.getElementById('education-timeline');
  const slider = document.querySelector('.tab-slider');
  if (type === 'work') {
    workTab.classList.add('active');
    eduTab.classList.remove('active');
    workTimeline.style.display = '';
    eduTimeline.style.display = 'none';
    if (slider) slider.style.transform = 'translateX(0%)';
  } else {
    workTab.classList.remove('active');
    eduTab.classList.add('active');
    workTimeline.style.display = 'none';
    eduTimeline.style.display = '';
    if (slider) slider.style.transform = 'translateX(100%)';
  }
}

// Animate slider on page load
window.addEventListener('DOMContentLoaded', () => {
  const slider = document.querySelector('.tab-slider');
  if (slider) slider.style.transform = 'translateX(0%)';
});

// Remove hash from URL after clicking footer quick links
document.querySelectorAll('.footer-links a').forEach(link => {
  link.addEventListener('click', function (e) {
    // Allow default jump to anchor
    setTimeout(() => {
      if (window.location.hash) {
        history.replaceState(null, '', window.location.pathname + window.location.search);
      }
    }, 0);
  });
});


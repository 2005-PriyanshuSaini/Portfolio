const greetings = [
  "• Hello", "• Hola", "• Bonjour", "• Ciao", "• Hallo", "• Olá", "• Salam",
  "• Hej", "• Nǐ hǎo", "• Konnichiwa", "• Annyeong", "• Merhaba", "• Shalom",
  "• Sawubona", "• Yā", "• Privet", "• Vanakkam", "• Sat Sri Akal",
];

const finalGreeting = "• नमस्ते";
const greetingElement = document.getElementById("greeting");

let index = 0;
let delay = 500;

function showNextGreeting() {
  if (index < greetings.length) {
    greetingElement.textContent = greetings[index];
    index++;
    delay *= 0.85; // speed up
    setTimeout(showNextGreeting, delay);
  } else {
    greetingElement.textContent = finalGreeting;
  }
}

window.onload = () => {
  setTimeout(showNextGreeting, delay);
};

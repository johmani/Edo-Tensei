var backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--background-color');
var primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color');
var secondaryColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary-color');
var tertiaryColor = getComputedStyle(document.documentElement).getPropertyValue('--tertiary-color');
var fourthColor = getComputedStyle(document.documentElement).getPropertyValue('--fourth-color');
var hoverColor = getComputedStyle(document.documentElement).getPropertyValue('--hover-color');
var textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-color');


// var toolSwitch = document.querySelector('.mode-switch');
// toolSwitch.addEventListener('click', function () {
//     document.documentElement.classList.toggle('light');
//     toolSwitch.classList.toggle('active');
// });

const buttons = [importButton, pencilButton, textButton, moveButton, applyButton];

function setActive(button) {
  buttons.forEach((btn) => {
    if (btn !== button) {
      btn.classList.remove('active');
    }
  });
}

buttons.forEach((button) => {
  button.addEventListener('click', function () {
    button.classList.toggle('active');
    setActive(button);
  });
});

pencil_size_slider.addEventListener('input', () => (pencil_size_value.textContent = pencil_size_slider.value));
text_size_slider.addEventListener('input', () => (text_size_value.textContent = text_size_slider.value));

importButton.addEventListener("click", () => {
  
  document.body.style.cursor = "auto";
  scetchTool.setState(false);
  select.setState(false);

  items.forEach((item) => {
    item.setState(true);
  });
});


pencilButton.addEventListener("click", () => {

  pencilProperties.classList.toggle('active');
  textProperties.classList.remove('active');

  // document.body.style.cursor = "auto";

  scetchTool.setState(true);
  select.setState(false);



  items.forEach((item) => {
    item.isSelected = false;
    item.setState(false);
  });
});



textButton.addEventListener("click", () => {

  // textProperties.classList.toggle('active');
  pencilProperties.classList.remove('active');

  document.body.style.cursor = "crosshair";

  scetchTool.setState(false);
  select.setState(true);

  items.forEach((item) => {
    item.setState(true);
  });
});


moveButton.addEventListener("click", () => {
  
  document.body.style.cursor = "auto";

  scetchTool.setState(false);
  select.setState(false);

  items.forEach((item) => {
    item.setState(true);
  });

});

checkBoxGradient.checked = true;




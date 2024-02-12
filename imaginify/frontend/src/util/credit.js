export function getCredits() {
  let text_credit = -1;
  if (localStorage.getItem("text_credit")) {
    text_credit = localStorage.getItem("text_credit");
  }
  let image_credit = -1;
  if (localStorage.getItem("image_credit")) {
    image_credit = localStorage.getItem("image_credit");
  }
  return [text_credit, image_credit];
}

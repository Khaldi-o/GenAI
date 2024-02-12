import { redirect } from "react-router-dom";

export function action() {
  localStorage.removeItem("token");
  localStorage.removeItem("expiration");
  localStorage.removeItem("text_credit");
  localStorage.removeItem("image_credit");
  localStorage.removeItem("id");
  return redirect("/");
}

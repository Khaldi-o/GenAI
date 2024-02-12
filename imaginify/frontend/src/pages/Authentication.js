import AuthForm from "../components/AuthForm";
import { json, redirect } from "react-router-dom";

function AuthenticationPage() {
  return <AuthForm />;
}

export default AuthenticationPage;

export async function action({ request }) {
  const searchParams = new URL(request.url).searchParams;
  const mode = searchParams.get("mode") || "login";
  if (mode !== "login" && mode !== "signup") {
    throw json({ message: "Unsupported mode" }, { status: 422 });
  }
  const data = await request.formData();
  const authData = {
    email: data.get("email"),
    password: data.get("password"),
  };
  const url = `${process.env.REACT_APP_BACKEND_URL || "http://localhost:8080"}/`;

  const response = await fetch(url + mode, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(authData),
  });
  if (response.status === 422 || response.status === 401) {
    return response;
  }
  if (!response.ok) {
    throw json({ message: "Could not authenticate" }, { status: 500 });
  }
  const respData = await response.json();
  const token = respData.token;
  localStorage.setItem("token", token);
  const text_credit = respData.user.text_credit;
  const image_credit = respData.user.image_credit;
  const user_id = respData.user.id;
  localStorage.setItem("text_credit", text_credit);
  localStorage.setItem("image_credit", image_credit);
  localStorage.setItem("id", user_id);
  const expiration = new Date();
  expiration.setHours(expiration.getHours() + 1);
  localStorage.setItem("expiration", expiration.toISOString());
  return redirect("/");
}

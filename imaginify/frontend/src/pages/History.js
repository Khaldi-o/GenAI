import { getAuthToken } from "../util/auth";
import PostHistory from "../components/PostHistory";
import { json, redirect } from "react-router-dom";

export default function HistoryPage() {
  return <PostHistory />;
}

export async function loader({ request, params }) {
  const token = getAuthToken();
  if (!token) {
    return redirect("/auth");
  }
  const userId = params.userId;
  let url =
    `${process.env.REACT_APP_BACKEND_URL || "http://localhost:8080"}/posts/` +
    userId;

  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
      Accept: "application/json",
    },
  });

  if (response.status === 422) {
    return response;
  }

  if (!response.ok) {
    throw json({ message: "Could not generate new post." }, { status: 500 });
  }

  const respData = await response.json();
  return respData;
}

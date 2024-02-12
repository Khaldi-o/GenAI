import { useSelector, useDispatch } from "react-redux";
import ImageGrid from "../components/ImageGrid";
import { Fragment } from "react";
import Preview from "../components/Preview";
import { getAuthToken } from "../util/auth";
import { json, redirect } from "react-router-dom";
import { previewActions } from "../store/preview-slice";

export default function PostPage() {
  const postData = useSelector((state) => state.post.postData);
  const openPreview = useSelector((state) => state.preview.openPreview);
  const dispatch = useDispatch();
  dispatch(
    previewActions.writeData({
      text: postData.text,
      network: postData.network,
      subject: postData.subject,
    }),
  );
  // const handleOpenPreview = () => {
  //     dispatch(previewActions.openPreview());
  // }
  return (
    <Fragment>
      <Preview open={openPreview} />
      <div className="flex flex-row min-h-screen w-full">
        <div className="flex-1 w-1/2 h-3/4 flex flex-col justify-center items-center p-12">
          <h1 className="text-3xl"> Text suggestion </h1>
          <div className="w-full h-1/2 overflow-auto mt-16">
            {" "}
            {/* Wrapper for p tag */}
            <p>{postData.text}</p>
            {/* <button className='button' onClick={handleOpenPreview}> Preview </button> */}
          </div>
        </div>
        <div className="flex-1 w-1/2 h-3/4 flex flex-col justify-center items-center p-12">
          <h1 className="text-3xl"> Images </h1>
          <div className="mt-16">
            <ImageGrid images={postData.images} />
          </div>
        </div>
      </div>
    </Fragment>
  );
}

export async function action({ request, params }) {
  const method = request.method;
  const data = await request.formData();

  const network = data.get("network");
  const postData = {
    network: network,
    text: data.get("text"),
    image: data.get("url"),
    subject: data.get("subject"),
  };

  let url = `${process.env.REACT_APP_BACKEND_URL || "http://localhost:8080"}/save`;

  const token = getAuthToken();
  const response = await fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
      Accept: "application/json",
    },
    body: JSON.stringify(postData),
  });

  if (response.status === 422) {
    return response;
  }

  if (!response.ok) {
    throw json({ message: "Could not generate new post." }, { status: 500 });
  }

  const user_id = localStorage.getItem("id");
  return redirect("/history/" + user_id);
}

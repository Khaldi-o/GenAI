import { useSelector, useDispatch } from "react-redux";
import ImageGrid from "../components/ImageGrid";
import { Fragment } from "react";
import Preview from "../components/Preview";
import { getAuthToken } from "../util/auth";
import { json, redirect, useActionData, useNavigate} from "react-router-dom";
import { previewActions } from "../store/preview-slice";
import { useEffect } from "react";
import _ from 'underscore';

export default function PostPage() {
  const postData = useSelector((state) => state.post.postData);
  const openPreview = useSelector((state) => state.preview.openPreview);
  const previewData  = useSelector((state) => state.preview.previewData, _.isEqual);
  const dispatch = useDispatch();
  const data = useActionData();
  const navigate = useNavigate();

  useEffect(() => {
    console.log('previezData', previewData, data);
    if (data && data.images){
      console.log('images data',data, previewData);
      dispatch(previewActions.writeData(data));
    }
  }, [dispatch, data, previewData]);
  dispatch(
    previewActions.writeData({
      text: postData.text,
      network: postData.network,
      subject: postData.subject,
      images: postData.images,
  
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
            <p>{previewData.text}</p>
            {/* <button className='button' onClick={handleOpenPreview}> Preview </button> */}
          </div>
        </div>
        <div className="flex-1 w-1/2 h-3/4 flex flex-col justify-center items-center p-12">
          <h1 className="text-3xl"> Images </h1>
          <div className="mt-16">
            <ImageGrid images={previewData.images} />
          </div>
        </div>
      </div>
    </Fragment>
  );
}

export async function action({ request, params }) {
  const method = request.method;
  console.log('save',request.save);
  const data = await request.formData();
  
  const intent = data.save;
  if (intent) {
      console.log('intent',intent);
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
  else {
    let url = `${process.env.REACT_APP_BACKEND_URL || "http://localhost:8080"}/`;
  url =
    url + `${process.env.REACT_APP_REAL_CALLS === "true" ? "content/image" : "test"}`;
    console.log('data in else', data);
    for (let [key, value] of data) {
      console.log(`${key}: ${value}`)
    }
  const token = getAuthToken();
  const network = data.get("network");
  const postData = {
    network: network,
    image_prompt: data.get("image_prompt"),
  };
  const response = await fetch(url, {
    method: 'post',
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
      Accept: "application/json",
    },
    body: JSON.stringify(postData),
  });

  if (response.status === 422) {
    console.log(await response.json());
    return await  response.json();
  }

  if (!response.ok) {
    throw json({ message: "Could not generate images." }, { status: 500 });
  }

  const respData = await response.json();
  localStorage.setItem("image_credit", respData.image_credit);
  return respData;
  }

}

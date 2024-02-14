import {
  Form,
  useNavigate,
  useNavigation,
  useActionData,
  useState,
  json,
} from "react-router-dom";
import classes from "./NewPostForm.module.css";
import { getAuthToken } from "../util/auth";
import { postActions } from "../store/post-slice";
import { useDispatch } from "react-redux";
import { useEffect } from "react";
import { SOCIAL_MEDIA, SOCIAL_MEDIA_CHAR_LIM } from "../util/social-network";
import { LANGUAGE } from "../util/languages";
import { getCredits } from "../util/credit";

function NewPostForm({ method }) {
  const dispatch = useDispatch();
  const data = useActionData();
  const navigate = useNavigate();
  // const submit = useSubmit();
  const navigation = useNavigation();

  // const [textLoading, setTextLoading] = useState(false);  
  // const [imgLoading, setImgLoading] = useState(false);   
  useEffect(() => {
   
    if (data && data.text) {
       console.log("DATA", data);
      dispatch(postActions.writeData(data));
      navigate("/post");
  }}, [data, dispatch, navigate]);

  const isSubmitting = navigation.state === "submitting";

  function cancelHandler() {
    navigate("..");
  }

  const [text_credit] = getCredits();

  return (
    <Form method={method} className={classes.form}>
      {data && data.errors && (
        <ul>
          {Object.values(data.errors).map((err) => (
            <li key={err}>{err}</li>
          ))}
        </ul>
      )}
      <h2 className="text-base mb-1 text-[#6ec530] uppercase font-bold">
        Create your new post!
      </h2>
      <p className="text-xl mb-1 text-[#9bafaf]">
        Let's start creating new content 🚀{" "}
      </p>

      <fieldset required>
        <legend className="text-sm text-[#9bafaf] uppercase">
          Select your social network
        </legend>
        <div className={classes.network}>
          <label htmlFor={SOCIAL_MEDIA.LINKEDIN}>LinkedIn</label>
          <input
            type="radio"
            id={SOCIAL_MEDIA.LINKEDIN}
            name="network"
            value={SOCIAL_MEDIA.LINKEDIN}
            required
          />
        </div>
        <div className={classes.network}>
          <label htmlFor={SOCIAL_MEDIA.TWITTER}>Twitter(X)</label>
          <input
            type="radio"
            id={SOCIAL_MEDIA.TWITTER}
            name="network"
            value={SOCIAL_MEDIA.TWITTER}
            required
          />
        </div>
        <div className={classes.network}>
          <label htmlFor={SOCIAL_MEDIA.INSTAGRAM}>Instagram</label>
          <input
            type="radio"
            id={SOCIAL_MEDIA.INSTAGRAM}
            name="network"
            value={SOCIAL_MEDIA.INSTAGRAM}
          />
        </div>

        <div className={classes.network}>
          <label htmlFor={SOCIAL_MEDIA.FACEBOOK}>Facebook</label>
          <input
            type="radio"
            id={SOCIAL_MEDIA.FACEBOOK}
            name="network"
            value={SOCIAL_MEDIA.FACEBOOK}
          />
        </div>
        <div className={classes.network}>
          <label htmlFor={SOCIAL_MEDIA.BLOG}>Blog</label>
          <input
            type="radio"
            id={SOCIAL_MEDIA.BLOG}
            name="network"
            value={SOCIAL_MEDIA.BLOG}
          />
        </div>
      </fieldset>
      <div className="mt-2">
        <label htmlFor="subject">Content topic</label>
        <textarea id="subject" type="subject" name="subject" required />
      </div>
      <div className="mt-2">
        <label htmlFor="style">Content style </label>
        <select id="style" type="style" name="style" required>
          <option value=""> Select an option</option>
          <option value="professional">professional</option>
          <option value="quirky">quirky</option>
          <option value="educational">educational</option>
          <option value="funny">funny</option>
          <option value="analytic">analytic</option>
          <option value="prospective">prospective</option>
          <option value="inspiring">inspiring</option>
          <option value="innovative">innovative</option>
          <option value="avant-garde">avant-garde</option>
          <option value="critic">critic</option>
          <option value="engaging">engaging</option>
        </select>
      </div>
      <div className="mt-2">
        <label htmlFor="content">Content</label>
        <textarea id="content" type="content" name="content" required />
      </div>
      <div className="mt-2">
        <label htmlFor="characters">Number of characters</label>
        <input
          type="number"
          id="characters"
          name="characters"
          min="0"
          step="1"
        />
        {data && data.warning && <p className="text-red-600">{data.warning}</p>}
      </div>
      <div className="mt-2">
        <label htmlFor="language"> Request language</label>
        <select id="language" type="language" name="language" required>
          <option value=""> Select an option</option>
          <option value={LANGUAGE.ENGLISH}>English</option>
          <option value={LANGUAGE.FRENCH}>Français</option>
        </select>
      </div>

      <div className="mt-2">
        <label htmlFor="outputLanguage">Generated posts language</label>
        <select id="outputLanguage" name="outputLanguage" required>
          <option value="">Select an option</option>
          <option value={LANGUAGE.ENGLISH}>English</option>
          <option value={LANGUAGE.FRENCH}>Français</option>
        </select>
      </div>

      <div className={classes.actions}>
        <button type="reset" disabled={isSubmitting}>
          Reset
        </button>
        <button type="button" onClick={cancelHandler} disabled={isSubmitting}>
          Cancel
        </button>
        <button disabled={isSubmitting}>
          {isSubmitting ? "Submitting..." : `Generate - ${text_credit}🪙`}
        </button>
      </div>
    </Form>
  );
}

export default NewPostForm;

export async function action({ request, params }) {
  const method = request.method;
  const data = await request.formData();
  const network = data.get("network");
  const characters = data.get("characters");


  if (
    network === SOCIAL_MEDIA.LINKEDIN &&
    +characters > SOCIAL_MEDIA_CHAR_LIM.LINKEDIN
  ) {
    return json(
      {
        warning: `${characters} is above ${SOCIAL_MEDIA_CHAR_LIM.LINKEDIN}, the maximum number of characters authorized on ${SOCIAL_MEDIA.LINKEDIN}.`,
      },
      { status: 422 }
    );
  }
  if (
    network === SOCIAL_MEDIA.TWITTER &&
    +characters > SOCIAL_MEDIA_CHAR_LIM.TWITTER
  ) {
    return json(
      {
        warning: `${characters} is above ${SOCIAL_MEDIA_CHAR_LIM.TWITTER}, the maximum number of characters authorized on ${SOCIAL_MEDIA.TWITTER}.`,
      },
      { status: 422 }
    );
  }
  if (
    network === SOCIAL_MEDIA.INSTAGRAM &&
    +characters > SOCIAL_MEDIA_CHAR_LIM.INSTAGRAM
  ) {
    return json(
      {
        warning: `${characters} is above ${SOCIAL_MEDIA_CHAR_LIM.INSTAGRAM}, the maximum number of characters authorized on ${SOCIAL_MEDIA.INSTAGRAM}.`,
      },
      { status: 422 }
    );
  }
  if (
    network === SOCIAL_MEDIA.FACEBOOK &&
    +characters > SOCIAL_MEDIA_CHAR_LIM.FACEBOOK
  ) {
    return json(
      {
        warning: `${characters} is above ${SOCIAL_MEDIA_CHAR_LIM.FACEBOOK}, the maximum number of characters authorized on ${SOCIAL_MEDIA.FACEBOOK}.`,
      },
      { status: 422 }
    );
  }
  if (
    network === SOCIAL_MEDIA.BLOG &&
    +characters > SOCIAL_MEDIA_CHAR_LIM.BLOG
  ) {
    return json(
      {
        warning: `${characters} is above ${SOCIAL_MEDIA_CHAR_LIM.BLOG}, the maximum number of characters authorized on ${SOCIAL_MEDIA.BLOG}.`,
      },
      { status: 422 }
    );
  }
  const newPostData = {
    network: network,
    subject: data.get("subject"),
    style: data.get("style"),
    content: data.get("content"),
    nb_characters: characters,
    language: data.get("language"),
    OutputLanguage: data.get("outputLanguage"),
  };
  let respData;
  let url = `${process.env.REACT_APP_BACKEND_URL || "http://localhost:8080"}/`;
  let text_url =
    url + `${process.env.REACT_APP_REAL_CALLS === "true" ? "content/text" : "test"}`;
  let img_url =
    url + `${process.env.REACT_APP_REAL_CALLS === "true" ? "content/image" : "test"}`;
  const token = getAuthToken();
    // do something
    return fetch(text_url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
        Accept: "application/json",
      },
      body: JSON.stringify(newPostData),
    }).then(async function(response) {
      if (response.status === 422) {
      return response;
    }
  
    if (!response.ok) {
      throw json({ message: "Could not generate new post." }, { status: 500 });
    }
  
    try {
      respData = await response.json();
      
     
    localStorage.setItem("text_credit", response.text_credit);
    localStorage.setItem("image_credit", response.image_credit);
    respData.foo = 'bar';
    return respData;
      
    }finally {
      var data = respData;
      console.log('finally', data, Object.isExtensible(data));
      let input = {...respData};
      let response = await fetch(img_url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
          Accept: "application/json",
        },
        body: JSON.stringify(input),
      })
     if (response.status === 422) {
        return response;
     }
      if (!response.ok) {
        throw json({ message: "Could not generate new post." }, { status: 500 });
      }
    let respData2 = await response.json();  // Corrected variable name
    console.log('finally', data, Object.isExtensible(data));
    //data.images = respData2.images;
    console.log(data);
    // localStorage.setItem("text_credit", respData.text_credit);
    // localStorage.setItem("image_credit", respData.image_credit);
    // localStorage.setItem("resp", JSON.stringify(respData));
      }
    })
}

import { previewActions } from "../../store/preview-slice";
import { useDispatch, useSelector } from "react-redux";
import { useSubmit } from "react-router-dom";
import { useState, useRef } from "react";
import PostLikeHeader from "./PostLikeHeader";

export default function LinkedInPostLayout({ ...props }) {
  const dispatch = useDispatch();
  const submit = useSubmit();
  const [edit, setEdit] = useState(false);
  const previewData = useSelector((state) => state.preview.previewData);
  const paragraphRef = useRef();
  const [textareaHeight, setTextareaHeight] = useState("auto");

  const handleEdit = () => {
    setEdit((state) => !state);
    if (paragraphRef.current) {
      setTextareaHeight(`${paragraphRef.current.offsetHeight}px`);
    }
  };
  const handleTextChanges = (event) => {
    dispatch(previewActions.editText(event));
  };
  const handlePost = () => {
    const proceed = window.confirm("Save in catalog?");
    if (proceed) {
      dispatch(previewActions.closePreview());
      submit(previewData, { method: "post" });
    }
  };
  const handleClose = () => {
    dispatch(previewActions.closePreview());
  };
  return (
    <div className="flex flex-col bg-white border border-gray-200 rounded-lg shadow-md overflow-hidden max-w-md mx-auto">
      <PostLikeHeader
        data={previewData}
        edit={edit}
        height={textareaHeight}
        onChange={handleTextChanges}
        ref={paragraphRef}
      />
      <div className="flex justify-end p-4">
        <button
          onClick={handleEdit}
          className="mr-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300"
        >
          {edit ? "Save" : "Edit"}
        </button>

        <button
          onClick={handleClose}
          className="mr-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300"
        >
          Close
        </button>
        <button
          onClick={handlePost}
          className={`px-4 py-2 text-white rounded transition duration-300 ${
            edit
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-700"
          }`}
          disabled={edit}
        >
          Save the post
        </button>
      </div>
    </div>
  );
}

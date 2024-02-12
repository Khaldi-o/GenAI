import CopyToClipboardButton from "./CopyToClipboardButton";
import PostLikeHeader from "./UI/PostLikeHeader";

export default function PostItem({ post }) {
  const image = `${
    process.env.REACT_APP_BACKEND_URL || "http://localhost:8080"
  }/${post.imagePath}`;
  const data = {
    text: post.text,
    url: image,
  };
  return (
    <li key={post.id}>
      <div className="flex flex-col bg-white border border-gray-200 rounded-lg shadow-md overflow-hidden max-w-md mx-auto">
        <article className="max-h-[60vh] overflow-y-auto">
          <h3 className="text-stone-900 text-center font-semibold">
            {post.subject}
          </h3>

          <PostLikeHeader
            data={data}
            edit={false}
            height="150px"
          ></PostLikeHeader>
          <div className="flex justify-end p-4">
            <CopyToClipboardButton textToCopy={post.text}>
              {" "}
              Copy to clipboard{" "}
            </CopyToClipboardButton>
            <CopyToClipboardButton textToCopy={image}>
              {" "}
              Copy image url to clipboard{" "}
            </CopyToClipboardButton>
          </div>
        </article>
      </div>
    </li>
  );
}

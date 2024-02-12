import { forwardRef } from "react";

const UserAvatar =
  "https://cdn.iconscout.com/icon/free/png-512/free-person-1768015-1502189.png?f=webp&w=256";
const UserName = "Avatar";

const PostLikeHeader = forwardRef(function PostLikeHeader(
  { data, edit, height, onChange },
  ref,
) {
  const userName = UserName;
  const userAvatar = UserAvatar;
  const handleTextChanges = (event) => {
    onChange(event.target.value);
  };

  return (
    <>
      <div className="flex items-start p-4 h-3/4">
        <img
          src={userAvatar}
          alt="User Avatar"
          className="rounded-full w-12 h-12 mr-4"
        />
        <div className="w-full">
          <div className="font-bold">{userName}</div>
          <div className="text-stone-900 w-full overflow-auto">
            {!edit && (
              <p ref={ref} className="text-sm">
                {data.text}
              </p>
            )}
            {edit && (
              <textarea
                className="w-full text-sm"
                style={{ height: height }}
                id="postText"
                name="postText"
                value={data.text}
                onChange={handleTextChanges}
              />
            )}
          </div>
        </div>
      </div>

      {data.url && (
        <img src={data.url} alt="Post" className="w-full h-auto object-cover" />
      )}
      <div className="flex justify-between items-center p-4 border-t">
        <span>💬 Reply</span>
        <span>🔁 Retweet</span>
        <span>❤️ Like</span>
        <span>🔗 Share</span>
      </div>
    </>
  );
});

export default PostLikeHeader;

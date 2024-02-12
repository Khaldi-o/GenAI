import { useLoaderData } from "react-router-dom";
import classes from "./PostHistory.module.css";
import PostItem from "./PostItem";

export default function PostHistory() {
  const postHistory = useLoaderData();
  return (
    <ul id={classes.posts}>
      {postHistory.map((post) => (
        <PostItem post={post} key={post.id} />
      ))}
    </ul>
  );
}

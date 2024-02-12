import classes from "./Background.module.css";

export default function BackgroundImg({ children, image_path, ...props }) {
  return <div className={classes.containerImg}>{children}</div>;
}

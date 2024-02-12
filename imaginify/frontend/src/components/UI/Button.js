import classes from "./Button.module.css";

export default function Button({ children, ...props }) {
  return (
    <button onClick={props.onClick} className={classes.button}>
      {children}
    </button>
  );
}

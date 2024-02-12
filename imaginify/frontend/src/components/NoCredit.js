import classes from "./NoCredit.module.css";

export default function NoCredit() {
  return (
    <div className={classes.container}>
      <p>You exceeded your current quota</p>
    </div>
  );
}

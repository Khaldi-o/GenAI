import {
  Form,
  Link,
  useSearchParams,
  useActionData,
  useNavigation,
} from "react-router-dom";
import Button from "./UI/Button";
import classes from "./AuthForm.module.css";

function AuthForm() {
  const data = useActionData();
  const navigation = useNavigation();

  const [searchParams] = useSearchParams();

  const isLogin = searchParams.get("mode") === "login";
  const isSubmitting = navigation.state === "submitting";
  return (
    <>
      <Form method="post" className={classes.form}>
        <h1>Welcome!</h1>
        <h2>{isLogin ? "Login to your account" : "Create a new account"}</h2>
        <p>
          <label htmlFor="email">Email</label>
          <input id="email" type="email" name="email" required />
        </p>
        {data && data.detail && (
          <ul>
            {" "}
            {Object.values(data.detail).map((err) => (
              <li key={err}> {err} </li>
            ))}{" "}
          </ul>
        )}
        <p>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            name="password"
            required
            className="text-stone-900"
          />
        </p>
        <div className={classes.actions}>
          <Link to={`?mode=${isLogin ? "signup" : "login"}`}>
            {isLogin ? "Sign Up" : "Login"}
          </Link>
          <Button disabled={isSubmitting}>
            {isSubmitting ? "Submitting..." : "OK"}
          </Button>
        </div>
      </Form>
    </>
  );
}

export default AuthForm;

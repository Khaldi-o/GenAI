import { Outlet, useLoaderData, useSubmit } from "react-router-dom";
import BackgroundImg from "../components/Background";
import MainNavigation from "../components/MainNavigation";
import Footer from "../components/Footer";
import { useEffect } from "react";
import { getTokenDuration } from "../util/auth";
import classes from "./Root.module.css";

function RootLayout() {
  const token = useLoaderData();
  const submit = useSubmit();
  useEffect(() => {
    if (!token) {
      return;
    }
    if (token === "EXPIRED") {
      submit(null, { action: "/logout", method: "post" });
      return;
    }
    const tokenDuration = getTokenDuration();
    setTimeout(() => {
      submit(null, { action: "/logout", method: "post" });
    }, tokenDuration);
  }, [token, submit]);
  return (
    <div className={classes.rootMainHeader}>
      <BackgroundImg image_path="./assets/back1.jpg">
        <MainNavigation />
        <main className={classes.main}>
          {/* {navigation.state === 'loading' && <p>Loading...</p>} */}
          <Outlet />
        </main>
      </BackgroundImg>

      <Footer className={classes.footer} />
    </div>
  );
}

export default RootLayout;
